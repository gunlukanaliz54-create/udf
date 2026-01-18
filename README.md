# 📄 UDF Evrak Görüntüleyici

Modern, web tabanlı mahkeme evrak görüntüleyici sistemi. UDF formatındaki evrakları PDF'e dönüştürür ve kullanıcı dostu bir arayüzde görüntüler.

## 🚀 Özellikler

### UDF → PDF Dönüştürücü

- ✅ UDF dosyalarını otomatik PDF'e dönüştürme
- 📝 Temiz, okunabilir PDF formatı
- 🇹🇷 Türkçe karakter desteği
- 🎨 Profesyonel görünüm

### Web Görüntüleyici

- 🖥️ Split-view tasarım (Sol: Liste, Sağ: PDF)
- 🔍 Anlık arama özelliği
- 📱 Responsive tasarım (Mobil, Tablet, Desktop)
- ⬇️ PDF indirme
- 🔗 Yeni sekmede açma
- ⌨️ Klavye kısayolları (ESC)

## 📁 Proje Yapısı

```
D:\dva\
├── evrak_viewer.html           # Ana web arayüzü
├── start_server.py             # Python web sunucusu
├── create_professional_pdf.py  # UDF → PDF dönüştürücü
├── convert_udf_to_pdf.py       # Alternatif dönüştürücü
├── udf_to_readable.py          # UDF → TXT dönüştürücü
├── scripts/                    # Yardımcı scriptler
├── evraklar_kaynak/            # Kaynak UDF dosyaları
├── evraklar_pdf/               # Dönüştürülmüş PDF'ler
├── evraklar_txt/               # TXT formatları
└── README.md                   # Bu dosya
```

## 🎯 Hızlı Başlangıç

### 1. Gereksinimler

```bash
# Python 3.x kurulu olmalı
python --version

# Gerekli kütüphaneler
pip install reportlab
```

### 2. UDF Dosyalarını PDF'e Dönüştürme

```bash
python create_professional_pdf.py
```

Bu komut:

- `evraklar_kaynak/` klasöründeki tüm UDF dosyalarını okur
- Profesyonel PDF'lere dönüştürür
- `evraklar_pdf/` klasörüne kaydeder

### 3. Web Sunucusunu Başlatma

```bash
python start_server.py
```

Tarayıcı otomatik açılacak: `http://localhost:8000/evrak_viewer.html`

## 📖 Kullanım

### Web Arayüzü

1. **Evrak Seçme**: Sol panelden bir evrak seçin
2. **Görüntüleme**: Sağ panelde PDF otomatik açılır
3. **Arama**: Üst kısımdaki arama kutusunu kullanın
4. **İndirme**: "İndir" butonuna tıklayın
5. **Yeni Sekme**: "Yeni Sekmede Aç" ile tam ekran görüntüleyin

### Klavye Kısayolları

- `ESC` - Sidebar'ı aç/kapat (mobilde)

## 🛠️ Teknik Detaylar

### UDF Format

UDF dosyaları, mahkeme evrak yönetim sistemlerinde kullanılan özel bir ZIP arşiv formatıdır:

- İçinde `content.xml` ve `documentproperties.xml` bulunur
- CDATA bloğunda gerçek içerik saklanır
- ODT (OpenDocument Text) benzeri yapı

### PDF Dönüştürme

```python
# UDF → XML → Temizleme → PDF
1. ZIP arşivini aç
2. content.xml'i parse et
3. CDATA içeriğini çıkar
4. Gereksiz karakterleri temizle
5. ReportLab ile PDF oluştur
```

### Web Teknolojileri

- **HTML5** - Yapı
- **CSS3** - Gradient, Flexbox, Grid
- **Vanilla JavaScript** - Dinamik içerik
- **Python HTTP Server** - Yerel sunucu

## 📊 İstatistikler

- **Toplam Evrak**: 16 adet
- **Dönüşüm Başarı**: %94 (16/17)
- **Ortalama PDF Boyutu**: ~75 KB
- **Desteklenen Format**: UDF (UYAP)

## 🔧 Özelleştirme

### Renk Teması Değiştirme

`evrak_viewer.html` içinde:

```css
/* Ana gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Kendi renklerinizi kullanın */
background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
```

### Yeni Evrak Ekleme

1. UDF dosyasını `evraklar_kaynak/` klasörüne kopyalayın
2. `python create_professional_pdf.py` komutunu çalıştırın
3. `evrak_viewer.html` içindeki `evraklar` dizisine ekleyin:

```javascript
const evraklar = [
  // Mevcut evraklar...
  { id: "evrak_YENI", dosya: "evraklar_pdf/evrak_YENI.pdf" },
];
```

## 🐛 Sorun Giderme

### PDF Görünmüyor

- Tarayıcınızın PDF desteğini kontrol edin
- Dosya yollarının doğru olduğundan emin olun
- Konsolu kontrol edin (F12)

### Port Hatası (8000 kullanımda)

`start_server.py` içinde PORT değiştirin:

```python
PORT = 8080  # Farklı bir port
```

### UDF Dönüştürme Hatası

- Python 3.x kurulu olduğundan emin olun
- `pip install reportlab` komutunu çalıştırın
- UDF dosyasının bozuk olmadığını kontrol edin

## 📱 Responsive Tasarım

### Desktop (>1024px)

- Sidebar: 400px genişlik
- Split-view görünüm
- Tam özellikler

### Tablet (768px - 1024px)

- Sidebar: 350px genişlik
- Optimize edilmiş düzen

### Mobil (<768px)

- Sidebar: Gizlenebilir (☰ butonu)
- Tam ekran PDF görüntüleme
- Touch-friendly butonlar

## 🔒 Güvenlik

⚠️ **Önemli**: Bu sistem yerel kullanım içindir.

İnternet üzerinden paylaşmak için:

- HTTPS kullanın
- Kimlik doğrulama ekleyin
- Dosya erişim kontrolü yapın
- CORS ayarlarını yapılandırın

## 📝 Lisans

Bu proje kişisel kullanım içindir.

## 👨‍💻 Geliştirici

**Hazırlayan**: Kiro AI Assistant  
**Tarih**: 18 Ocak 2026  
**Versiyon**: 1.0

## 🙏 Teşekkürler

- ReportLab - PDF oluşturma
- Python HTTP Server - Yerel sunucu
- Modern CSS - Responsive tasarım

---

**Not**: Hassas evraklar için ek güvenlik önlemleri alınmalıdır.
