import xml.etree.ElementTree as ET
from pathlib import Path
import zipfile
import re

def extract_text_from_odt_xml(xml_path):
    """ODT content.xml'den text çıkar"""
    try:
        tree = ET.parse(xml_path)
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
        return f"XML parse hatası: {e}"

def convert_udf_to_text(udf_file):
    """UDF dosyasını text'e dönüştür"""
    output_file = str(udf_file).replace('.udf', '.txt')
    
    try:
        # ZIP olarak aç
        with zipfile.ZipFile(udf_file, 'r') as zip_ref:
            # Geçici klasöre çıkar
            extract_dir = f"{udf_file.stem}_temp"
            zip_ref.extractall(extract_dir)
            
            # content.xml'i oku
            content_xml = Path(extract_dir) / 'content.xml'
            if content_xml.exists():
                text_content = extract_text_from_odt_xml(content_xml)
                
                # Text dosyasına yaz
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"{'='*60}\n")
                    f.write(f"Dosya: {udf_file.name}\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(text_content)
                
                print(f"✓ Dönüştürüldü: {output_file}")
                
                # Geçici klasörü temizle
                import shutil
                shutil.rmtree(extract_dir)
                
                return True
            else:
                print(f"✗ content.xml bulunamadı: {udf_file}")
                return False
                
    except Exception as e:
        print(f"✗ Hata ({udf_file}): {e}")
        return False

def convert_all_udf_files():
    """Tüm UDF dosyalarını dönüştür"""
    udf_files = list(Path('.').glob('*.udf'))
    
    if not udf_files:
        print("UDF dosyası bulunamadı!")
        return
    
    print(f"\n{len(udf_files)} adet UDF dosyası bulundu\n")
    
    success_count = 0
    for udf_file in udf_files:
        if convert_udf_to_text(udf_file):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Toplam: {len(udf_files)} dosya")
    print(f"Başarılı: {success_count} dosya")
    print(f"Başarısız: {len(udf_files) - success_count} dosya")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    convert_all_udf_files()
