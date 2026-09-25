import socket
import subprocess
import sys
import urllib.request
import json

def get_ngrok_url():
    try:
        req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            return data["tunnels"][0]["public_url"]
    except Exception:
        return None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def main():
    print("="*65)
    print("📱 [WAR ROOM LAUNCHER] Booting Remote Connection...")
    print("="*65)
    
    url = get_ngrok_url()
    if url:
        print(f"🌍 [NGROK DETECTED] Generating QR for Public Remote URL: {url}")
    else:
        url = f"http://{get_local_ip()}:8501"
        print(f"🏠 [WIFI ONLY] No ngrok tunnel found. Generating QR for Local IP: {url}")

    try:
        import qrcode
        qr = qrcode.QRCode(box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        print("\n📲 Scan this QR code with your mobile camera:\n")
        qr.print_ascii(invert=True)
    except ImportError:
        print("📦 Installing 'qrcode' package...")
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode"], capture_output=True)
        import qrcode
        qr = qrcode.QRCode(box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        print("\n📲 Scan this QR code with your mobile camera:\n")
        qr.print_ascii(invert=True)

    print("\n🚀 Launching Streamlit (WebSocket Compression Disabled for Mobile)...")
    subprocess.run([
        "streamlit", "run", "app.py", 
        "--server.port", "8501", 
        "--server.address", "0.0.0.0", 
        "--server.enableCORS", "false", 
        "--server.enableXsrfProtection", "false",
        "--server.enableWebsocketCompression", "false"
    ])

if __name__ == "__main__":
    main()
