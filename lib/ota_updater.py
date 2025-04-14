import urequests as requests
import machine
import io
import uzlib
from crypto import AES

KEY = b'1234567890abcdef'
NONCE = b'abcdef123456'

def decrypt(ciphertext):
    cipher = AES.new(KEY, AES.MODE_CTR, nonce=NONCE)
    return cipher.decrypt(ciphertext)

def download_and_install(url):
    try:
        print(f"Downloading encrypted update from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            encrypted = response.content
            zip_bytes = decrypt(encrypted)

            with uzlib.ZipFile(io.BytesIO(zip_bytes)) as z:
                z.extractall('/')
            print("Update applied. Rebooting...")
            machine.reset()
        else:
            print("Failed to download update, status:", response.status_code)
    except Exception as e:
        print("OTA update failed:", e)