import socket
import time
import machine  # Needed for reset
# NOTE: 'cfg' will be passed in from boot.py

def start_web_server(cfg):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('🌐 Web server running at 0.0.0.0:80')

    while True:
        client, addr = s.accept()
        print('📡 Client connected from', addr)
        try:
            client.settimeout(5.0)
            request = client.recv(1024).decode('utf-8')
            method = request.split(' ')[0]
            path = request.split(' ')[1]

            if method == 'GET' and path in ['/', '/index.html']:
                serve_config_form(client)
            elif method == 'POST' and path == '/save':
                handle_save_config(client, request, cfg)
            else:
                send_response(client, "404 Not Found", "text/plain", "404 - Not Found")

        except Exception as e:
            print("Webserver error:", e)
        finally:
            client.close()

def serve_config_form(client):
    html = """<!DOCTYPE html>
<html>
<head><title>Configure GORK</title></head>
<body style="font-family:sans-serif;text-align:center;padding:2em;">
<h1>GORK Setup</h1>
<form action="/save" method="post">
    <label>Wi-Fi SSID:<br><input name="ssid" /></label><br><br>
    <label>Password:<br><input name="password" type="password" /></label><br><br>
    <label>Location:<br><input name="location" /></label><br><br>
    <button type="submit">Save & Reboot</button>
</form>
</body></html>"""
    send_response(client, "200 OK", "text/html", html)

def handle_save_config(client, request, cfg):
    try:
        body = request.split('\r\n\r\n', 1)[1]
        params = {}
        for pair in body.split('&'):
            key, value = pair.split('=')
            params[key] = value.replace('+', ' ').strip()

        ssid = params.get('ssid', '')
        password = params.get('password', '')
        location = params.get('location', '')

        print("Saving config:", ssid, password, location)
        success = cfg.save_config(ssid, password, location)

        if success:
            html = "<html><body><h1>✅ Config Saved!</h1><p>Rebooting in 3 seconds...</p></body></html>"
            send_response(client, "200 OK", "text/html", html)
            time.sleep(3)
            machine.reset()
        else:
            raise Exception("Config save failed")

    except Exception as e:
        print("Failed to save config:", e)
        send_response(client, "500 Internal Server Error", "text/plain", "Failed to save configuration")

def send_response(client, status, content_type, body):
    response = f"""HTTP/1.1 {status}\r
Content-Type: {content_type}\r
\r
{body}"""
    client.send(response.encode())
