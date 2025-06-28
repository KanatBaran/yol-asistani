# Yapay Zeka Destekli Sürücü Yardımcısı

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/) [![License: Personal Use Only](https://img.shields.io/badge/License-Personal%20Use%20Only-red.svg)](LICENSE) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## İçindekiler

1. [Proje Özeti](#proje-özeti)
2. [Başlıca Özellikler](#başlıca-özellikler)
3. [Teknolojiler ve Mimari](#teknolojiler-ve-mimari)
4. [Proje Dizini](#proje-dizini)
6. [Lisans](#lisans)



## Proje Özeti

Gerçek zamanlı göz ve yüz ifadesi takibi ile sürücünün yorgunluk ve duygu durumunu algılayan, uyku veya stres tespit edildiğinde sesli uyarı ve müzikle güvenliği destekleyen yapay zeka tabanlı bir asistan.



## Başlıca Özellikler

* **Gerçek Zamanlı Göz Takibi:** MediaPipe Face Mesh kullanılarak EAR (Eye Aspect Ratio) hesaplanır ve uzun süreli göz kapanmalarıyla uyku hali tespit edilir.
* **Canlı Duygu Analizi:** OpenCV ile yüz bölgesi algılanır, TensorFlow/Keras tabanlı CNN modeli (FER2013) duygu sınıflandırması yapar.
* **Sesli Uyarılar & Müzik:** PyGame mixer üzerinden yorgunluk uyarısı, stres veya mutsuzluk gibi durumlarda uygun melodiler oynatılır.
* **Ses Seviyesi Kontrolü:** Pycaw kütüphanesi ile sistem ses düzeyi izlenir ve gerektiğinde otomatik ayarlama yapılır.
* **Anlık Konsol Çıktısı:** Göz kırpma sayısı, duygu durumu, ses seviyesi gibi bilgiler komut satırına yazdırılır.



## Teknolojiler ve Mimari

* **Python 3.7+**
* **OpenCV**: Görüntü yakalama ve ön işleme
* **MediaPipe**: Yüz ve göz noktalarını tespiti
* **TensorFlow/Keras**: Duygu sınıflandırma modeli
* **PyGame**: Ses oynatma
* **Pycaw**: Windows ses API entegrasyonu

Model eğitimi ve testleri FER2013 veri seti kullanılarak gerçekleştirilmiştir. Ana uygulama `main.py` üzerinden çalıştırılır.


## Proje Dizini

```
surucu-yardimcisi/           # Ana proje klasörü <br>
├── Models/                  # Eğitilmiş model ve sınıflayıcı dosyaları<br>
│   ├── model.h5             # CNN duygu analizi modeli<br>
│   └── haarcascade_frontalface_default.xml  # Yüz tespiti<br>
├── Sounds/                  # Uyarı ve müzik dosyaları<br>
│   ├── sleep_alert.mp3      # Uyku uyarısı sesi<br>
│   ├── angry.mp3            # Öfke halinde çalınacak müzik<br>
│   └── happy.mp3            # Mutluluk halinde çalınacak müzik<br>
├── main.py                  # Ana çalıştırma scripti<br>
├── requirements.txt         # Proje bağımlılıkları<br>
├── LICENSE                  # Lisans dosyası<br>
└── README.md                # Proje açıklaması (bu dosya)<br>
```

## Lisans

Bu proje yalnızca **kişisel kullanım** amaçlıdır. Ticari veya toplu dağıtım için kullanıma izin verilmez. Detaylı şartlar için `LICENSE` dosyasını inceleyebilirsiniz.
