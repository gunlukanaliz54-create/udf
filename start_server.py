import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS ve PDF görüntüleme için gerekli header'lar
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Web sunucusunu başlat"""
    
    # Mevcut dizini kontrol et
    if not Path('evrak_viewer.html').exists():
        print("✗ evrak_viewer.html bulunamadı!")
        return
    
    if not Path('evraklar_pdf').exists():
        print("✗ evraklar_pdf klasörü bulunamadı!")
        return
    
    # Sunucuyu başlat
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/evrak_viewer.html"
            
            print("="*60)
            print(f"🚀 Evrak Görüntüleyici Başlatıldı!")
            print("="*60)
            print(f"\n📍 Adres: {url}")
            print(f"📁 Dizin: {os.getcwd()}")
            print(f"\n✅ Tarayıcı otomatik açılacak...")
            print(f"\n⚠️  Durdurmak için: CTRL+C\n")
            print("="*60)
            
            # Tarayıcıyı aç
            webbrowser.open(url)
            
            # Sunucuyu çalıştır
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n✓ Sunucu durduruldu.")
    except OSError as e:
        if "address already in use" in str(e).lower():
            print(f"\n✗ Port {PORT} zaten kullanımda!")
            print(f"Alternatif: http://localhost:{PORT}/evrak_viewer.html adresini tarayıcıda açın")
        else:
            print(f"\n✗ Hata: {e}")

if __name__ == "__main__":
    start_server()
