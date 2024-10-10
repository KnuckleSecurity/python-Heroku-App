from flask import Flask, request, render_template_string, send_file, abort
import requests
import json
import os

app = Flask(__name__)

# Kullanıcı IP'sinden konum bilgisi alma fonksiyonu
def get_location(ip):
    try:
        # ipinfo.io veya başka bir API'den IP bilgisi al
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

# Ziyaretçilerin IP adresini ve konum bilgilerini dosyaya yazma
def log_visitor(ip, location):
    log_data = {
        'ip': ip,
        'location': location
    }
    
    # Ziyaretçi bilgilerini bir dosyaya yaz
    with open('visitor_logs.json', 'a') as log_file:
        log_file.write(json.dumps(log_data) + "\n")

# Anasayfa yönlendirmesi
@app.route('/')
def index():
    ip = request.remote_addr  # Ziyaretçinin IP adresini al
    location = get_location(ip)  # IP'den konum bilgisi al
    
    log_visitor(ip, location)  # IP ve konum bilgisini dosyaya kaydet

    # Sayfa Şu Anda İnşa Ediliyor mesajı ile karanlık tema
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ON DEVELOPMENT...</title>
        <style>
            body {
                background-color: #000;
                color: #ff0000;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 3em;
                text-shadow: 2px 2px 8px rgba(255, 0, 0, 0.8);
            }
        </style>
    </head>
    <body>
        <h1>ON DEVELOPMENT...</h1>
    </body>
    </html>
    """
    return render_template_string(html_content)

# Ziyaretçi loglarını gösteren yeni endpoint
@app.route('/visitors')
def visitors():
    # visitor_logs.json dosyasının olup olmadığını kontrol et
    if os.path.exists('visitor_logs.json'):
        return send_file('visitor_logs.json', as_attachment=False)
    else:
        abort(404, description="visitor_logs.json dosyası bulunamadı")

if __name__ == "__main__":
    # Flask sunucusunu belirli bir IP ve portta başlat
    app.run(host="192.168.1.109", port=5000, debug=True)
