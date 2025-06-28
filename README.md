# Yapay Zeka Destekli Sürücü Yardımcısı

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/) [![License: Personal Use Only](https://img.shields.io/badge/License-Personal%20Use%20Only-red.svg)](LICENSE)]\([https://www.python.org/](https://www.python.org/)) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## İçindekiler

1. [Proje Özeti](#proje-özeti)
2. [Başlıca Özellikler](#başlıca-özellikler)
3. [Teknolojiler ve Mimari](#teknolojiler-ve-mimari)
4. [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)
5. [Yapılandırma Seçenekleri](#yapılandırma-seçenekleri)
6. [Proje Dizini](#proje-dizini)
7. [Katkıda Bulunma](#katkıda-bulunma)
8. [Lisans](#lisans)

---

## Proje Özeti

Gerçek zamanlı göz ve yüz ifadesi takibi ile sürücünün yorgunluk ve duygu durumunu algılayan, uyku veya stres tespit edildiğinde sesli uyarı ve müzikle güvenliği destekleyen yapay zeka tabanlı bir asistan.

---

## Başlıca Özellikler

* **Gerçek Zamanlı Göz Takibi:** MediaPipe Face Mesh kullanılarak EAR (Eye Aspect Ratio) hesaplanır ve uzun süreli göz kapanmalarıyla uyku hali tespit edilir.
* **Canlı Duygu Analizi:** OpenCV ile yüz bölgesi algılanır, TensorFlow/Keras tabanlı CNN modeli (FER2013) duygu sınıflandırması yapar.
* **Sesli Uyarılar & Müzik:** PyGame mixer üzerinden yorgunluk uyarısı, stres veya mutsuzluk gibi durumlarda uygun melodiler oynatılır.
* **Ses Seviyesi Kontrolü:** Pycaw kütüphanesi ile sistem ses düzeyi izlenir ve gerektiğinde otomatik ayarlama yapılır.
* **Anlık Konsol Çıktısı:** Göz kırpma sayısı, duygu durumu, ses seviyesi gibi bilgiler komut satırına yazdırılır.

---

## Teknolojiler ve Mimari

* **Python 3.7+**
* **OpenCV**: Görüntü yakalama ve ön işleme
* **MediaPipe**: Yüz ve göz noktalarını tespiti
* **TensorFlow/Keras**: Duygu sınıflandırma modeli
* **PyGame**: Ses oynatma
* **Pycaw**: Windows ses API entegrasyonu

Model eğitimi ve testleri FER2013 veri seti kullanılarak gerçekleştirilmiştir. Ana uygulama `main.py` üzerinden çalıştırılır.

---

## Kurulum ve Çalıştırma

1. Depoyu klonlayın:

   ```bash
   git clone https://github.com/kullanici_adi/surucu-yardimcisi.git
   cd surucu-yardimcisi
   ```
2. Sanal ortam oluşturun ve etkinleştirin (isteğe bağlı ama önerilir):

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. Gerekli paketleri yükleyin:

   ```bash
   pip install -r requirements.txt
   ```
4. Uygulamayı başlatın:

   ```bash
   python main.py --camera 0 --model Models/model.h5
   ```

   Burada `--camera` ile kullanılacak kamera indeksini, `--model` ile duygu analizi modelinin yolunu belirleyebilirsiniz.

---

## Yapılandırma Seçenekleri

Aşağıdaki parametreleri `main.py` içinden veya komut satırı argümanlarıyla özelleştirebilirsiniz:

| Değişken              | Açıklama                                           | Varsayılan |
| --------------------- | -------------------------------------------------- | ---------- |
| `EAR_THRESHOLD`       | Göz kapalı kabul edilecek EAR eşik değeri          | `0.21`     |
| `CLOSED_FRAMES_LIMIT` | Sürekli kapalı çerçeve sayısı (uyku uyarısı eşiği) | `15`       |
| `EMOTION_CATEGORIES`  | Sınıflandırılacak duygu kategorileri               | `6`        |

---

## Proje Dizini

```
surucu-yardimcisi/           # Ana proje klasörü
├── Models/                  # Eğitilmiş model ve sınıflayıcı dosyaları
│   ├── model.h5             # CNN duygu analizi modeli
│   └── haarcascade_frontalface_default.xml  # Yüz tespiti
├── Sounds/                  # Uyarı ve müzik dosyaları
│   ├── sleep_alert.mp3      # Uyku uyarısı sesi
│   ├── angry.mp3            # Öfke halinde çalınacak müzik
│   └── happy.mp3            # Mutluluk halinde çalınacak müzik
├── main.py                  # Ana çalıştırma scripti
├── requirements.txt         # Proje bağımlılıkları
├── LICENSE                  # Lisans dosyası
└── README.md                # Proje açıklaması (bu dosya)
```

---

## Katkıda Bulunma

1. Forklayın (`Fork`)
2. Yeni bir branch oluşturun (`git checkout -b feature/yenilik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik ekle'`)
4. Branch’ınıza push edin (`git push origin feature/yenilik`)
5. Pull request açın

Projeye katkılarınız için teşekkürler! 🎉

---

## Lisans

Bu proje yalnızca **kişisel kullanım** amaçlıdır. Ticari veya toplu dağıtım için kullanıma izin verilmez. Detaylı şartlar için `LICENSE` dosyasını inceleyebilirsiniz.
