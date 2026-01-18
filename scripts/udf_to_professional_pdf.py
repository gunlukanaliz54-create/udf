from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import xml.etree.ElementTree as ET
from pathlib import Path
import zipfile
import re

class ODTParser:
    """ODT dosyasını parse et ve yapılandırılmış veri çıkar"""
    
    def __init__(self, udf_file):
        self.udf_file = udf_file
        self.content = {}
        
    def extract_content(self):
        """ODT içeriğini çıkar"""
        try:
            with zipfile.ZipFile(self.udf_file, 'r') as zip_ref:
                # content.xml'i oku
                with zip_ref.open('content.xml') as xml_file:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Namespace tanımları
                    namespaces = {
                        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
                        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
                    }
                    
                    # Body içeriğini bul
                    body = root.find('.//office:body/office:text', namespaces)
                    
                    if body is not None:
                        self.parse_body(body, namespaces)
                        
            return self.content
            
        except Exception as e:
            print(f"Parse hatası: {e}")
            return None
    
    def parse_body(self, body, ns):
        """Body içeriğini parse et"""
        paragraphs = []
        tables = []
        
        for elem in body:
            tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            
            if tag == 'p':
                # Paragraf
                text = self.get_text_recursive(elem)
                if text.strip():
                    paragraphs.append(text.strip())
                    
            elif tag == 'table':
                # Tablo
                table_data = self.parse_table(elem, ns)
                if table_data:
                    tables.append(table_data)
        
        self.content = {
            'paragraphs': paragraphs,
            'tables': tables
        }
    
    def get_text_recursive(self, element):
        """Element ve alt elementlerden text topla"""
        texts = []
        if element.text:
            texts.append(element.text)
        for child in element:
            texts.append(self.get_text_recursive(child))
            if child.tail:
                texts.append(child.tail)
        return ''.join(texts)
    
    def parse_table(self, table_elem, ns):
        """Tablo parse et"""
        rows = []
        for row in table_elem.findall('.//table:table-row', ns):
            cells = []
            for cell in row.findall('.//table:table-cell', ns):
                cell_text = self.get_text_recursive(cell)
                cells.append(cell_text.strip())
            if any(cells):  # Boş satırları atla
                rows.append(cells)
        return rows if rows else None


class ProfessionalPDFCreator:
    """Profesyonel PDF oluşturucu"""
    
    def __init__(self):
        # Türkçe font desteği
        try:
            pdfmetrics.registerFont(TTFont('Turkish', 'C:/Windows/Fonts/arial.ttf'))
            pdfmetrics.registerFont(TTFont('TurkishBold', 'C:/Windows/Fonts/arialbd.ttf'))
            self.font_name = 'Turkish'
            self.font_bold = 'TurkishBold'
        except:
            self.font_name = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'
    
    def create_styles(self):
        """PDF stilleri oluştur"""
        styles = getSampleStyleSheet()
        
        # Başlık stili
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontName=self.font_bold,
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            borderWidth=2,
            borderColor=colors.HexColor('#333333'),
            borderPadding=10
        ))
        
        # Alt başlık
        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading2'],
            fontName=self.font_bold,
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            alignment=TA_LEFT
        ))
        
        # Normal metin
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontName=self.font_name,
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_LEFT,
            leading=14
        ))
        
        # Vurgu metni
        styles.add(ParagraphStyle(
            name='CustomHighlight',
            parent=styles['Normal'],
            fontName=self.font_bold,
            fontSize=11,
            textColor=colors.HexColor('#c0392b'),
            spaceAfter=10,
            alignment=TA_CENTER
        ))
        
        return styles
    
    def create_pdf(self, udf_file, content):
        """PDF oluştur"""
        pdf_file = str(udf_file).replace('.udf', '_professional.pdf')
        
        # PDF dökümanı
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Stiller
        styles = self.create_styles()
        story = []
        
        # Başlık
        story.append(Paragraph(
            f"<b>EVRAK BELGESI</b>",
            styles['CustomTitle']
        ))
        story.append(Spacer(1, 0.5*cm))
        
        # Dosya bilgisi
        story.append(Paragraph(
            f"<i>Dosya: {udf_file.name}</i>",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 0.3*cm))
        
        # Paragrafları işle
        if 'paragraphs' in content:
            for para in content['paragraphs']:
                # Özel başlıkları tespit et
                if any(keyword in para.upper() for keyword in ['T.C.', 'ALINDI BELGESİ', 'UYAP']):
                    story.append(Paragraph(
                        f"<b>{para}</b>",
                        styles['CustomHeading']
                    ))
                elif ':' in para:
                    # Alan: Değer formatı
                    parts = para.split(':', 1)
                    if len(parts) == 2:
                        story.append(Paragraph(
                            f"<b>{parts[0]}:</b> {parts[1].strip()}",
                            styles['CustomBody']
                        ))
                    else:
                        story.append(Paragraph(para, styles['CustomBody']))
                else:
                    story.append(Paragraph(para, styles['CustomBody']))
                
                story.append(Spacer(1, 0.2*cm))
        
        # Tabloları işle
        if 'tables' in content and content['tables']:
            story.append(Spacer(1, 0.5*cm))
            for table_data in content['tables']:
                if table_data:
                    # Tablo oluştur
                    t = Table(table_data, colWidths=[doc.width/len(table_data[0])]*len(table_data[0]))
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), self.font_bold),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
                        ('FONTNAME', (0, 1), (-1, -1), self.font_name),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 0.5*cm))
        
        # PDF'i oluştur
        doc.build(story)
        return pdf_file


def convert_all_udf_to_professional_pdf():
    """Tüm UDF dosyalarını profesyonel PDF'e dönüştür"""
    udf_files = list(Path('.').glob('*.udf'))
    
    if not udf_files:
        print("UDF dosyası bulunamadı!")
        return
    
    print(f"\n{'='*60}")
    print(f"Profesyonel PDF Dönüştürücü")
    print(f"{'='*60}\n")
    print(f"{len(udf_files)} adet UDF dosyası bulundu\n")
    
    parser = ODTParser(None)
    pdf_creator = ProfessionalPDFCreator()
    
    success_count = 0
    for udf_file in udf_files:
        try:
            print(f"İşleniyor: {udf_file.name}")
            
            # Parse et
            parser.udf_file = udf_file
            content = parser.extract_content()
            
            if content:
                # PDF oluştur
                pdf_file = pdf_creator.create_pdf(udf_file, content)
                print(f"  ✓ Oluşturuldu: {Path(pdf_file).name}")
                success_count += 1
            else:
                print(f"  ✗ İçerik çıkarılamadı")
                
        except Exception as e:
            print(f"  ✗ Hata: {e}")
    
    print(f"\n{'='*60}")
    print(f"Toplam: {len(udf_files)} dosya")
    print(f"Başarılı: {success_count} PDF")
    print(f"Başarısız: {len(udf_files) - success_count} dosya")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    convert_all_udf_to_professional_pdf()
