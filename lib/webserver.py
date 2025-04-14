import socket
import network
import json
import os
import time
import machine

AP_IP = "192.168.4.1"

def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Web server listening on', addr)

    while True:
        client, addr = s.accept()
        print('Client connected from', addr)
        try:
            client.settimeout(5.0)
            request = client.recv(1024)
            request = request.decode('utf-8')

            # Extract method and path
            method = request.split(' ')[0]
            path = request.split(' ')[1]

            print('Method:', method, 'Path:', path)

            # Captive portal probe detection
            if "hotspot-detect.html" in request:
                print("iPhone captive portal detected, sending redirect...")
                redirect(client)
                continue

            if any(p in request for p in ["generate_204", "ncsi.txt", "connectivitycheck"]):
                print("Captive portal probe detected, sending redirect...")
                redirect(client)
                continue

            # Serve setup page
            if method == "GET" and (path == "/" or path == "/index.html"):
                serve_setup_page(client)
                continue

            # Handle configuration form submission
            if method == "POST" and path == "/save":
                save_configuration(client, request)
                continue

            # Fallback - redirect unknown paths
            redirect(client)

        except Exception as e:
            print('Webserver error:', e)
        finally:
            client.close()

def redirect(client):
    response = """HTTP/1.1 302 Found\r
Location: http://{}/\r
Content-Type: text/html\r
\r
<html><head><title>Redirect</title></head><body><h1>Redirecting...</h1></body></html>
""".format(AP_IP)
    client.send(response.encode())
    client.close()

def serve_setup_page(client):
    html = """<!DOCTYPE html>
<html>
<head>
    <title>GORK Presence Sensor Setup</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 20px; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);}
        h1 { text-align: center; color: #333; }
        label { display: block; margin-top: 20px; color: #555; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; }
        button { margin-top: 20px; width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 16px; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Configure GORK</h1>
        <form action="/save" method="post">
            <label>Wi-Fi SSID</label>
            <input type="text" name="ssid" required>

            <label>Wi-Fi Password</label>
            <input type="password" name="password" required>

            <label>Location (Room Name)</label>
            <input type="text" name="location" required>

            <button type="submit">Save & Connect</button>
        </form>
    </div>
</body>
</html>
"""
    response = """HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
""" + html
    client.send(response.encode())
    client.close()

def save_configuration(client, request):
    print('Saving configuration...')

    try:
        # Parse the POST body manually
        body = request.split('\r\n\r\n', 1)[1]
        params = {}
        for pair in body.split('&'):
            key, value = pair.split('=')
            params[key] = value.replace('+', ' ').strip()

        ssid = params.get('ssid', '')
        password = params.get('password', '')
        location = params.get('location', '')

        config = {
            'ssid': ssid,
            'password': password,
            'location': location
        }

        with open('config.json', 'w') as f:
            json.dump(config, f)

        print('Config saved:', config)

        # Return success page
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Success</title>
    <meta http-equiv="refresh" content="5; url=http://{}/">
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>🎉 GORK Configured Successfully!</h1>
    <p>Rebooting to connect to Wi-Fi...</p>
</body>
</html>
""".format(AP_IP)

        response = """HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
""" + html
        client.send(response.encode())

        time.sleep(2)
        machine.reset()

    except Exception as e:
        print('Failed to save configuration:', e)
        client.close()
