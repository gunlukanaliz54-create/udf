import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

# Namespace tanımları
NAMESPACES = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
}

def extract_structured_content_from_udf(udf_file):
    """UDF dosyasından yapılandırılmış içerik çıkar"""
    try:
        with zipfile.ZipFile(udf_file, 'r') as zip_ref:
            # content.xml'i oku
            xml_content = zip_ref.read('content.xml').decode('utf-8')
            
            # CDATA içeriğini çıkar
            cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', xml_content, re.DOTALL)
            
            if cdata_match:
                text_content = cdata_match.group(1)
            else:
                # CDATA yoksa tüm metni al
                tree = ET.fromstring(xml_content)
                text_content = ''.join(tree.itertext())
            
            # İçeriği satırlara böl ve temizle
            lines = text_content.split('\n')
            clean_lines = []
            
            for line in lines:
                line = line.strip()
                if line and line not in ['', ' ']:
                    clean_lines.append(line)
            
            return clean_lines
                
    except Exception as e:
        print(f"Parse hatası: {e}")
        import traceback
        traceback.print_exc()
        return None

def clean_text(text):
    """Metni temizle - gereksiz karakterleri kaldır"""
    # HTML/XML tag'lerini temizle
    text = re.sub(r'<[^>]+>', '', text)
    # Çoklu boşlukları tek boşluğa indir
    text = re.sub(r'\s+', ' ', text)
    # Placeholder metinleri temizle
    text = re.sub(r'(evrakinGittigiMahkeme|dosyaNo|aciklama|geldigiYerKisi|ilgiliKisi|tarihSaat|icraSikayet)', '', text)
    # Gereksiz karakterleri temizle
    text = text.replace('□', '').strip()
    return text

def create_professional_pdf(udf_file, output_dir):
    """Profesyonel görünümlü PDF oluştur"""
    
    pdf_filename = udf_file.stem + '.pdf'
    pdf_path = output_dir / pdf_filename
    
    try:
        # İçeriği çıkar
        lines = extract_structured_content_from_udf(udf_file)
        if not lines:
            print(f"✗ İçerik çıkarılamadı: {udf_file.name}")
            return False
        
        # PDF oluştur
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Türkçe font kaydet
        try:
            pdfmetrics.registerFont(TTFont('Turkish', 'C:/Windows/Fonts/arial.ttf'))
            pdfmetrics.registerFont(TTFont('Turkish-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
        except:
            pass
        
        # Stiller
        styles = getSampleStyleSheet()
        
        # Başlık stili
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Turkish-Bold' if 'Turkish-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=20,
            spaceBefore=10
        )
        
        # Normal metin stili
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName='Turkish' if 'Turkish' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            alignment=TA_LEFT,
            spaceAfter=8,
            leading=14
        )
        
        # Vurgu stili
        emphasis_style = ParagraphStyle(
            'CustomEmphasis',
            parent=normal_style,
            fontName='Turkish-Bold' if 'Turkish-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#000000'),
            spaceAfter=10
        )
        
        # PDF içeriği
        story = []
        
        # Başlık - ilk satırlar
        if len(lines) > 0:
            # İlk 5 satırı başlık olarak al
            header_lines = []
            for i, line in enumerate(lines[:5]):
                clean_line = clean_text(line)
                if clean_line:
                    header_lines.append(clean_line)
            
            if header_lines:
                story.append(Paragraph('<br/>'.join(header_lines), title_style))
                story.append(Spacer(1, 0.5*cm))
        
        # İçerik - kalan satırlar
        for line in lines[5:]:
            text = clean_text(line)
            
            # Boş satırları atla
            if not text or text in ['', ' ']:
                continue
            
            # Önemli başlıkları vurgula
            if any(keyword in text for keyword in ['ALINDI BELGESİ', 'Evrakın Gönderildiği', 'Yukarıda bilgileri']):
                story.append(Spacer(1, 0.3*cm))
                story.append(Paragraph(text, emphasis_style))
                story.append(Spacer(1, 0.2*cm))
            else:
                # Etiket ve değer ayrımı yap
                if ':' in text:
                    parts = text.split(':', 1)
                    label = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else ''
                    
                    if value:
                        formatted_text = f"<b>{label}:</b> {value}"
                    else:
                        formatted_text = f"<b>{label}</b>"
                    
                    story.append(Paragraph(formatted_text, normal_style))
                else:
                    story.append(Paragraph(text, normal_style))
        
        # PDF'i oluştur
        doc.build(story)
        print(f"✓ PDF oluşturuldu: {pdf_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Hata ({udf_file.name}): {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_all_udf_to_professional_pdf():
    """Tüm UDF dosyalarını profesyonel PDF'e dönüştür"""
    
    source_dir = Path('evraklar_kaynak')
    output_dir = Path('evraklar_pdf')
    
    if not source_dir.exists():
        print(f"✗ Kaynak klasör bulunamadı: {source_dir}")
        return
    
    # Eski PDF'leri temizle
    if output_dir.exists():
        for old_pdf in output_dir.glob('*.pdf'):
            old_pdf.unlink()
        print("✓ Eski PDF'ler temizlendi\n")
    
    output_dir.mkdir(exist_ok=True)
    
    udf_files = list(source_dir.glob('*.udf'))
    
    if not udf_files:
        print(f"✗ {source_dir} klasöründe UDF dosyası bulunamadı!")
        return
    
    print(f"{len(udf_files)} adet UDF dosyası bulundu\n")
    print("="*60)
    
    success_count = 0
    for udf_file in udf_files:
        if create_professional_pdf(udf_file, output_dir):
            success_count += 1
    
    print("="*60)
    print(f"\nToplam: {len(udf_files)} dosya")
    print(f"Başarılı: {success_count} PDF")
    print(f"Başarısız: {len(udf_files) - success_count} dosya")
    print(f"\nPDF'ler kaydedildi: {output_dir.absolute()}\n")

if __name__ == "__main__":
    try:
        import reportlab
        convert_all_udf_to_professional_pdf()
    except ImportError:
        print("✗ reportlab kütüphanesi kurulu değil!")
        print("\nKurmak için:")
        print("  pip install reportlab")
