from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import textwrap

def create_pdf_from_txt(txt_file):
    """Text dosyasını PDF'e dönüştür"""
    
    pdf_file = str(txt_file).replace('.txt', '.pdf')
    
    try:
        # PDF oluştur
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4
        
        # Türkçe karakter desteği için font (sistem fontunu kullan)
        try:
            # Windows için
            pdfmetrics.registerFont(TTFont('Turkish', 'C:/Windows/Fonts/arial.ttf'))
            c.setFont('Turkish', 10)
        except:
            # Font bulunamazsa varsayılan
            c.setFont('Helvetica', 10)
        
        # Text dosyasını oku
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Satırlara böl
        lines = content.split('\n')
        
        # Sayfa ayarları
        margin = 50
        y_position = height - margin
        line_height = 14
        
        for line in lines:
            # Satır çok uzunsa kes
            if len(line) > 80:
                wrapped_lines = textwrap.wrap(line, width=80)
            else:
                wrapped_lines = [line]
            
            for wrapped_line in wrapped_lines:
                # Sayfa sonu kontrolü
                if y_position < margin:
                    c.showPage()
                    try:
                        c.setFont('Turkish', 10)
                    except:
                        c.setFont('Helvetica', 10)
                    y_position = height - margin
                
                # Satırı yaz
                try:
                    c.drawString(margin, y_position, wrapped_line)
                except:
                    # Türkçe karakter sorunu varsa ASCII'ye çevir
                    c.drawString(margin, y_position, wrapped_line.encode('ascii', 'ignore').decode())
                
                y_position -= line_height
        
        # PDF'i kaydet
        c.save()
        print(f"✓ PDF oluşturuldu: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"✗ PDF oluşturma hatası ({txt_file}): {e}")
        return False

def convert_all_txt_to_pdf():
    """Tüm evrak TXT dosyalarını PDF'e dönüştür"""
    txt_files = list(Path('.').glob('evrak_*.txt'))
    
    if not txt_files:
        print("Evrak TXT dosyası bulunamadı!")
        return
    
    print(f"\n{len(txt_files)} adet TXT dosyası bulundu\n")
    
    success_count = 0
    for txt_file in txt_files:
        if create_pdf_from_txt(txt_file):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Toplam: {len(txt_files)} dosya")
    print(f"Başarılı: {success_count} PDF")
    print(f"Başarısız: {len(txt_files) - success_count} dosya")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # reportlab kurulu mu kontrol et
    try:
        import reportlab
        convert_all_txt_to_pdf()
    except ImportError:
        print("✗ reportlab kütüphanesi kurulu değil!")
        print("\nKurmak için:")
        print("  pip install reportlab")
