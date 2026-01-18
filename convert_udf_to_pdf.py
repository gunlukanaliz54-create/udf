import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap

def extract_text_from_udf(udf_file):
    """UDF dosyasından text çıkar"""
    try:
        with zipfile.ZipFile(udf_file, 'r') as zip_ref:
            # content.xml'i oku
            with zip_ref.open('content.xml') as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Tüm text node'ları topla
                texts = []
                for elem in root.iter():
                    if elem.text:
                        texts.append(elem.text.strip())
                    if elem.tail:
                        texts.append(elem.tail.strip())
                
                # Boş satırları temizle ve birleştir
                content = '\n'.join([t for t in texts if t])
                return content
    except Exception as e:
        return f"Hata: {e}"

def create_pdf_from_udf(udf_file, output_dir):
    """UDF dosyasını direkt PDF'e dönüştür"""
    
    # Çıktı dosya adı
    pdf_filename = udf_file.stem + '.pdf'
    pdf_path = output_dir / pdf_filename
    
    try:
        # UDF'den text çıkar
        content = extract_text_from_udf(udf_file)
        
        # PDF oluştur
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4
        
        # Türkçe karakter desteği
        try:
            pdfmetrics.registerFont(TTFont('Turkish', 'C:/Windows/Fonts/arial.ttf'))
            c.setFont('Turkish', 10)
        except:
            c.setFont('Helvetica', 10)
        
        # Başlık ekle
        c.setFont('Helvetica-Bold', 12)
        c.drawString(50, height - 40, f"Evrak: {udf_file.stem}")
        c.line(50, height - 45, width - 50, height - 45)
        
        # Normal font'a dön
        try:
            c.setFont('Turkish', 10)
        except:
            c.setFont('Helvetica', 10)
        
        # Satırlara böl
        lines = content.split('\n')
        
        # Sayfa ayarları
        margin = 50
        y_position = height - 70
        line_height = 14
        
        for line in lines:
            # Satır çok uzunsa kes
            if len(line) > 80:
                wrapped_lines = textwrap.wrap(line, width=80)
            else:
                wrapped_lines = [line] if line else ['']
            
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
        print(f"✓ PDF oluşturuldu: {pdf_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Hata ({udf_file.name}): {e}")
        return False

def convert_all_udf_to_pdf():
    """Tüm UDF dosyalarını PDF'e dönüştür"""
    
    # Kaynak ve hedef klasörler
    source_dir = Path('evraklar_kaynak')
    output_dir = Path('evraklar_pdf')
    
    if not source_dir.exists():
        print(f"✗ Kaynak klasör bulunamadı: {source_dir}")
        return
    
    # Çıktı klasörünü oluştur
    output_dir.mkdir(exist_ok=True)
    
    # UDF dosyalarını bul
    udf_files = list(source_dir.glob('*.udf'))
    
    if not udf_files:
        print(f"✗ {source_dir} klasöründe UDF dosyası bulunamadı!")
        return
    
    print(f"\n{len(udf_files)} adet UDF dosyası bulundu\n")
    print("="*60)
    
    success_count = 0
    for udf_file in udf_files:
        if create_pdf_from_udf(udf_file, output_dir):
            success_count += 1
    
    print("="*60)
    print(f"\nToplam: {len(udf_files)} dosya")
    print(f"Başarılı: {success_count} PDF")
    print(f"Başarısız: {len(udf_files) - success_count} dosya")
    print(f"\nPDF'ler kaydedildi: {output_dir.absolute()}\n")

if __name__ == "__main__":
    try:
        import reportlab
        convert_all_udf_to_pdf()
    except ImportError:
        print("✗ reportlab kütüphanesi kurulu değil!")
        print("\nKurmak için:")
        print("  pip install reportlab")
