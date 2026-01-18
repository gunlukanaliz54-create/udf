# 📄 Evrak Görüntüleyici Sistemi

Modern, kullanıcı dostu web tabanlı evrak görüntüleyici.

## 🚀 Özellikler

- ✅ **Modern Arayüz**: Gradient renkler ve animasyonlu kartlar
- 🔍 **Anlık Arama**: Evrak numarası veya tarih ile hızlı arama
- 📱 **Responsive**: Mobil, tablet ve masaüstü uyumlu
- 👁️ **Modal Görüntüleme**: PDF'leri sayfa içinde görüntüleme
- ⬇️ **İndirme**: Tek tıkla PDF indirme
- 📊 **İstatistikler**: Toplam ve filtrelenmiş evrak sayısı

## 📁 Dosya Yapısı

```
D:\dva\
├── evrak_viewer.html       # Ana HTML dosyası
├── start_server.py          # Python web sunucusu
├── evraklar_pdf\            # PDF dosyaları (16 adet)
│   ├── evrak_12452252045.pdf
│   ├── evrak_12452252046.pdf
│   └── ...
└── EVRAK_VIEWER_README.md   # Bu dosya
```

## 🎯 Kullanım

### Yöntem 1: Python Sunucu (Önerilen)

```bash
python start_server.py
```

Tarayıcı otomatik açılacak: `http://localhost:8000/evrak_viewer.html`

### Yöntem 2: Manuel

1. `evrak_viewer.html` dosyasını tarayıcıda aç
2. Veya herhangi bir web sunucusu kullan

## 🔧 Gereksinimler

- Python 3.x (sunucu için)
- Modern web tarayıcı (Chrome, Firefox, Edge, Safari)

## 📖 Nasıl Çalışır?

1. **Ana Sayfa**: Tüm evraklar kart formatında listelenir
2. **Arama**: Üst kısımdaki arama kutusuna evrak numarası yazın
3. **Görüntüleme**:
   - Karta tıklayın → Modal'da açılır
   - "Görüntüle" butonu → Yeni sekmede açılır
4. **İndirme**: "İndir" butonuna tıklayın

## 🎨 Özelleştirme

### Renk Teması Değiştirme

`evrak_viewer.html` dosyasında CSS bölümünde:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Gradient renklerini değiştirin.

### Yeni Evrak Ekleme

`evrak_viewer.html` içindeki `evraklar` dizisine ekleyin:

```javascript
const evraklar = [
  { id: "evrak_XXXXXXX", dosya: "evraklar_pdf/evrak_XXXXXXX.pdf" },
  // Yeni evrak buraya
];
```

## 🛑 Sunucuyu Durdurma

Terminal'de `CTRL+C` tuşlarına basın.

## 📊 İstatistikler

- **Toplam Evrak**: 16 adet
- **Format**: PDF
- **Ortalama Boyut**: ~75 KB
- **Kaynak**: UDF → PDF dönüşümü

## 🔒 Güvenlik Notları

- Bu sistem yerel kullanım içindir
- İnternet üzerinden paylaşmak için güvenlik önlemleri alın
- Hassas evraklar için erişim kontrolü ekleyin

## 💡 İpuçları

- **Hızlı Arama**: Evrak numarasının sadece bir kısmını yazın
- **Klavye Kısayolları**: ESC tuşu ile modal'ı kapatın
- **Mobil Kullanım**: Tam ekran için yatay mod kullanın

## 🐛 Sorun Giderme

### PDF Görünmüyor

- Tarayıcınızın PDF desteğini kontrol edin
- Dosya yollarının doğru olduğundan emin olun

### Port Hatası

- `start_server.py` içinde PORT değerini değiştirin
- Örnek: `PORT = 8080`

### Arama Çalışmıyor

- Tarayıcı konsolunu kontrol edin (F12)
- JavaScript hatalarını inceleyin

## 📞 Destek

Sorun yaşarsanız:

1. Tarayıcı konsolunu kontrol edin (F12)
2. Dosya yollarını doğrulayın
3. Python sürümünü kontrol edin: `python --version`

---

**Hazırlayan**: Kiro AI Assistant
**Tarih**: 18 Ocak 2026
**Versiyon**: 1.0
