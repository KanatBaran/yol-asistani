# BARAN KANAT - 22100011013

### KUTUPHANELER (START) ###
import cv2
import mediapipe as mp
import numpy as np
import math

#ses dosyasi icin kutuphaneler
import pygame
import time

#bilgisayarin hapörlerine ersebilmek icin
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
### KUTUPHANELER (END) ###

### FONKSIYONLAR (START) ###
# İki nokta arası Öklid mesafesi
def euclidean_distance(p1, p2):
    return math.dist(p1, p2)

# Göz açıklık oranı (EAR) hesaplama fonksiyonu
def compute_EAR(landmarks, indexes, w, h):
    # EAR için gerekli 6 noktanın koordinatlarını al
    p1 = (int(landmarks[indexes[0]].x * w), int(landmarks[indexes[0]].y * h))
    p2 = (int(landmarks[indexes[1]].x * w), int(landmarks[indexes[1]].y * h))
    p3 = (int(landmarks[indexes[2]].x * w), int(landmarks[indexes[2]].y * h))
    p4 = (int(landmarks[indexes[3]].x * w), int(landmarks[indexes[3]].y * h))
    p5 = (int(landmarks[indexes[4]].x * w), int(landmarks[indexes[4]].y * h))
    p6 = (int(landmarks[indexes[5]].x * w), int(landmarks[indexes[5]].y * h))

    # EAR formülü
    vertical1 = euclidean_distance(p2, p6)
    vertical2 = euclidean_distance(p3, p5)
    horizontal = euclidean_distance(p1, p4)

    if horizontal == 0:
        return 0  # bölme hatasına karşı koruma

    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

def printListe(liste):
    acik = 0
    kapali = 0
    for x in liste:
        if x == 0:
            kapali = kapali + 1
        elif x == 1:
            acik = acik + 1

    print(f"Goz Durum -> Acik: {acik}, Kapali:{kapali}")

#surekli olarak son 100 elemani tutar
def son100(liste):
    if len(liste) > 150:
        liste[:] = liste[-150:]


#bilgisayaarin ses duzeyini veren fonksiyon
def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar()

    return int(current_volume * 100)  # Yüzdelik döner

#ses artirma fonksiyonu
def increase_volume(step=0.05):  # step = %5 artırır
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = interface.QueryInterface(IAudioEndpointVolume)

    current = volume.GetMasterVolumeLevelScalar()  # 0.0 - 1.0 arası
    new_volume = min(current + step, 1.0)  # 1.0'ı geçmesin
    volume.SetMasterVolumeLevelScalar(new_volume, None)

    print(f"Yeni Ses Seviyesi: %{int(new_volume * 100)}")

#ses duzeyini ayarlama fonksiyonu
def set_volume(percent):
    # Yüzdelik değeri 0.0 - 1.0 arası değere çevir
    level = max(0.0, min(percent / 100, 1.0))

    # Hoparlörü bul ve ayarla
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(level, None)

    print(f"Ses seviyesi ayarlandı: %{int(level * 100)}")
### FONKSIYONLAR (END) ###


### DEGISKENLER (START) ###
# Göz kırpma sayacı ve eşik değerleri
blink_count = 0
closed_frames = 0
EAR_THRESHOLD = 0.23  # Göz kapalı kabul edilecek eşik
CLOSED_FRAMES_LIMIT = 2 # Arka arkaya kaç kare kapalı olursa kırpma say


# MediaPipe bileşenlerini başlat
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)  # Sadece bir yüzle çalış
mp_drawing = mp.solutions.drawing_utils  # Landmark çizimleri için

# Göz çevresi (görsel çizim için)
LEFT_EYE = [33, 160, 158, 133, 153, 144, 163, 7, 246]
RIGHT_EYE = [362, 385, 387, 263, 373, 380, 390, 249, 466]

# EAR hesaplama için 6 nokta (sabit)
LEFT_EYE_INDEXES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDEXES = [362, 385, 387, 263, 373, 380]

# Yüz yönü için yanak landmark'ları
LEFT_CHEEK = 234
RIGHT_CHEEK = 454

# Uyku Kontrol #
eye_status_list = [] # Göz durumu geçmişi (liste olarak)
alarmCal = 0 # alarm kontrol degiskenidir. 0 = alarm calmiyor

# Pygame ses motorunu başlat
pygame.mixer.init()
# Ses dosyasını yükle
sound = pygame.mixer.Sound("Sounds/sleepAlert.mp3")  # MP3 veya WAV olabilir

# ./Uyku Kontrol #
### DEGISKENLER (END) ###


# Kamera başlat
cap = cv2.VideoCapture(0)



### ANA DÖNGÜ ###
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # BGR'den RGB'ye çevir (MediaPipe böyle istiyor)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Yüz mesh sonuçlarını al
    results = face_mesh.process(rgb_frame)

    # Yüz bulunduysa işle
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            # Yüz yönünü ölç (yana bakma açısı)
            left_x = face_landmarks.landmark[LEFT_CHEEK].x
            right_x = face_landmarks.landmark[RIGHT_CHEEK].x
            yaw_ratio = abs(left_x - right_x)

            # Göz noktalarını çiz (görsel olarak)
            for idx in LEFT_EYE + RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # EAR hesapla
            left_ear = compute_EAR(face_landmarks.landmark, LEFT_EYE_INDEXES, w, h)
            right_ear = compute_EAR(face_landmarks.landmark, RIGHT_EYE_INDEXES, w, h)
            avg_ear = (left_ear + right_ear) / 2

            #print(f"EAR: {avg_ear:.3f}, Closed frames: {closed_frames}, Blinks: {blink_count}")

            # Göz kırpma kontrolü
            if avg_ear < EAR_THRESHOLD:
                closed_frames += 1
                eye_status_list.append(0) #goz listesine kapali duumunu ekliyor
                print("Göz Kapalı")
            else:
                if closed_frames >= CLOSED_FRAMES_LIMIT:
                    blink_count += 1
                closed_frames = 0
                eye_status_list.append(1) #goz listesine kapali durumu ekliyor
                print("Göz Açık")

            #listeyi yazdir
            printListe(eye_status_list)

            #sürekli olarak son 100 elemanı tut
            son100(eye_status_list)
            print(f"Mevcut Ses Seviyesi: %{get_current_volume()}")

            if eye_status_list.count(0) > 100:
                alarmCal = 1
            else:
                alarmCal = 0

            if alarmCal == 1 and sound.get_num_channels() == 0:
                set_volume(20)
                sound.play(loops=-1)
            elif alarmCal == 1:
                increase_volume(0.0005)
            elif alarmCal == 0 and eye_status_list.count(0) < 30:
                sound.stop()


            # Durumu yazdır
            status = "Kapali" if avg_ear < EAR_THRESHOLD else "Acik"
            cv2.putText(frame, f"Goz Durumu: {status}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"Kirpma Sayisi: {blink_count}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 100), 2)
            #cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)


    # Kamerayı göster
    cv2.imshow("MediaPipe Eye Tracking", frame)

    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Kamera ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
