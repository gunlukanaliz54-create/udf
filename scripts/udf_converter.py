import os
import sys
from pathlib import Path

def analyze_udf_file(filepath):
    """UDF dosyasını analiz et ve içeriğini çözmeye çalış"""
    
    with open(filepath, 'rb') as f:
        # İlk 1024 byte'ı oku
        header = f.read(1024)
        
        # Dosya imzasını kontrol et
        print(f"Dosya: {filepath}")
        print(f"Boyut: {os.path.getsize(filepath)} bytes")
        print(f"\nİlk 100 byte (hex):")
        print(header[:100].hex())
        
        print(f"\nİlk 200 karakter (text deneme):")
        try:
            print(header[:200].decode('utf-8', errors='ignore'))
        except:
            print(header[:200].decode('latin-1', errors='ignore'))
        
        # PDF kontrolü
        if header.startswith(b'%PDF'):
            print("\n✓ Bu bir PDF dosyası!")
            return 'pdf'
        
        # ZIP/DOCX kontrolü
        if header.startswith(b'PK\x03\x04'):
            print("\n✓ Bu bir ZIP arşivi (DOCX/XLSX olabilir)!")
            return 'zip'
        
        # XML kontrolü
        if header.startswith(b'<?xml') or b'<' in header[:10]:
            print("\n✓ Bu bir XML dosyası olabilir!")
            return 'xml'
        
        # RTF kontrolü
        if header.startswith(b'{\\rtf'):
            print("\n✓ Bu bir RTF dosyası!")
            return 'rtf'
        
        print("\n? Bilinmeyen format")
        return 'unknown'

def convert_to_text(filepath, output_path):
    """Dosyayı text formatına dönüştürmeye çalış"""
    
    file_type = analyze_udf_file(filepath)
    
    if file_type == 'pdf':
        new_name = output_path.replace('.txt', '.pdf')
        os.rename(filepath, new_name)
        print(f"\n✓ PDF olarak kaydedildi: {new_name}")
        
    elif file_type == 'zip':
        new_name = output_path.replace('.txt', '.zip')
        import shutil
        shutil.copy(filepath, new_name)
        print(f"\n✓ ZIP olarak kaydedildi: {new_name}")
        print("  DOCX veya XLSX olabilir, uzantıyı değiştirip deneyin")
        
    elif file_type == 'xml':
        with open(filepath, 'rb') as f:
            content = f.read()
        with open(output_path, 'wb') as f:
            f.write(content)
        print(f"\n✓ XML olarak kaydedildi: {output_path}")
        
    else:
        # Ham içeriği text olarak kaydet
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # UTF-8 ve Latin-1 dene
        for encoding in ['utf-8', 'latin-1', 'cp1254']:
            try:
                text = content.decode(encoding)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"\n✓ Text olarak kaydedildi ({encoding}): {output_path}")
                return
            except:
                continue
        
        # Hiçbiri işe yaramazsa hex dump yap
        with open(output_path, 'w') as f:
            f.write(content.hex())
        print(f"\n✓ Hex dump olarak kaydedildi: {output_path}")

if __name__ == "__main__":
    # Tüm UDF dosyalarını işle
    udf_files = list(Path('.').glob('*.udf'))
    
    if not udf_files:
        print("UDF dosyası bulunamadı!")
        sys.exit(1)
    
    print(f"{len(udf_files)} adet UDF dosyası bulundu\n")
    print("="*60)
    
    for udf_file in udf_files:
        print(f"\n{'='*60}")
        output_name = str(udf_file).replace('.udf', '_converted.txt')
        convert_to_text(str(udf_file), output_name)
        print("="*60)
