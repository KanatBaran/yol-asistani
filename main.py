# BARAN KANAT - 22100011013


##### KUTUPHANELER (START) #####
import cv2 # kamera icin kutuphane
import mediapipe as mp # yuz tespiti icin
import numpy as np # hizli ve verimli matematiksel islemler icin
import math # matematiksel islemler icin

#ses dosyasi icin kutuphaneler
import pygame
import pygame.mixer

#zaman kutuphanesi
import time

#bilgisayarin hapörlerine ersebilmek icin
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Duygu analizi icin kutuphaneler
from tensorflow.keras.models import load_model # model calistirabilmek icin

#Terminali kullanabilmek icin gerekli kutuphane
import sys
##### KUTUPHANELER (END) #####


##### FONKSIYONLAR (START) #####
# ---- Yeni: Durum satırını konsola yazdıran fonksiyon ----
def print_status(blink_count, eye_status_list, volume, curr_emo, emo_counts):
    """
    Blink sayısı, göz durumu, ses seviyesi ve duygu özetini tek satırda günceller.
    """
    eye_open   = eye_status_list.count(1)
    eye_closed = eye_status_list.count(0)
    angry, fear, happy, neutral, sad, surprise = emo_counts

    status_line = (
        f"[Blink:{blink_count}] "
        f"Eyes-> O:{eye_open} C:{eye_closed} | "
        f"Vol:{volume}% | "
        f"Emo-> {curr_emo} "
        f"(A:{angry},F:{fear},H:{happy},N:{neutral},S:{sad},Su:{surprise})"
    )
    # \r ile satırı başa al ve üzerine yaz
    sys.stdout.write('\r' + status_line)
    sys.stdout.flush()


#--------- GozTakip ---------#
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

# Goz durum listesini yazdiran fonksiyon
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
#--------- ./GozTakip ---------#


#--------- DuyguAnalizi ---------#
# Son dugyu ortalamasina gore duygu analizi
def CurrentEmotion(list, threshold = 50):
    angry = fear = happy = neutral = sad = surprise = 0

    for x in list:
        if x == 'angry':
            angry += 1
        elif x == 'fear':
            fear += 1
        elif x == 'happy':
            happy += 1
        elif x == 'neutral':
            neutral += 1
        elif x == 'sad':
            sad += 1
        elif x == 'surprise':
            surprise += 1

    if angry > threshold:
        return 'angry'
    elif fear > threshold:
        return 'fear'
    elif happy > threshold:
        return 'happy'
    elif sad > threshold:
        return 'sad'
    elif surprise > threshold:
        return 'surprise'
    else:
        return 'neutral'


#listenin son 100 elemanini liste olarak dondurur
def listEnd(list, end = 100):
    newList = list[-end:]
    return newList

# duygularin sayisi hesaplayip yazdiran fonksiyon
def printListEmotion(list):
    angry = fear = happy = neutral = sad = surprise = 0

    for x in list:
        if x == 'angry':
            angry += 1
        elif x == 'fear':
            fear += 1
        elif x == 'happy':
            happy += 1
        elif x == 'neutral':
            neutral += 1
        elif x == 'sad':
            sad += 1
        elif x == 'surprise':
            surprise += 1

    #print(f'Sinirli: {angry}, Korku: {fear}, Mutlu: {happy}, Nötr: {neutral}, Üzgün: {sad}, Şaşkın: {surprise}')

# Duygu tahmini yapan fonksiyon
def analyze_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
    results = []

    for (x, y, w, h) in faces:
        face_img = image[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (96, 96))
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        face_img = face_img.astype("float32") / 255.0
        face_input = np.expand_dims(face_img, axis=0)
        prediction = model.predict(face_input, verbose=0)
        label = classes[np.argmax(prediction)]
        results.append((label, (x, y, w, h)))

    return results
#--------- ./DuyguAnalizi ---------#
##### FONKSIYONLAR (END) #####


##### AYARLAR (START) #####
# Pygame ses motorunu başlat
pygame.mixer.init()
##### AYARLAR (END) #####


##### DEGISKENLER (START) #####
#--------- GozTakip ---------#
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

# Ses dosyasını yükle
sound = pygame.mixer.Sound("Sounds/sleepAlert.mp3")  # Kullanicinin uyku sirasinda calisacak alarm
#--------- ./GozTakip ---------#


#--------- DuyguAnalizi ---------#
# MODEL
model = load_model("Models/model.h5")
classes = ['angry', 'angry', 'happy', 'neutral', 'sad', 'surprise']
detector = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')

listEmotion = [] # Kullanicinin duygusu bu listede tutulacaktir
listEmotionEnd = [] # Kullanicinin son 100 duygusu

# Ses dosyasını yükle
soundAngry = pygame.mixer.Sound("Sounds/Angry.mp3") # kullanicinin sinirli oldugu durumda caliacak 'rahatlatici' muzik
soundSad = pygame.mixer.Sound("Sounds/Sad.mp3") # kullanici uzgunken calacak 'tempolu' muzik

# duygu ses kontrolleri
isAngrySound = 0 # 'rahatlatici' muzik calinip calinmadigini kontrol eder.
isSadSound = 0 # 'tempolu' muzik calinip calinmadigini kontrol eder.
#--------- ./DuyguAnalizi ---------#
##### DEGISKENLER (END) #####


##### MAIN (START) #####
# Kamera başlat
cap = cv2.VideoCapture(0)

while True:
    # Kameradan kare oku
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
            left_ear  = compute_EAR(face_landmarks.landmark, LEFT_EYE_INDEXES,  w, h)
            right_ear = compute_EAR(face_landmarks.landmark, RIGHT_EYE_INDEXES, w, h)
            avg_ear   = (left_ear + right_ear) / 2

            # Göz kırpma kontrolü
            if avg_ear < EAR_THRESHOLD:
                closed_frames += 1
                eye_status_list.append(0)  # göz listesine kapalı durumunu ekliyor
                #print("Göz Kapalı")
            else:
                if closed_frames >= CLOSED_FRAMES_LIMIT:
                    blink_count += 1
                closed_frames = 0
                eye_status_list.append(1)  # göz listesine açık durumunu ekliyor
                #print("Göz Açık")

            # Listeyi yazdır
            printListe(eye_status_list)

            # Sürekli olarak son 100 elemanı tut
            son100(eye_status_list)
            #print(f"Mevcut Ses Seviyesi: %{get_current_volume()}")

            # Alarm durumu
            if eye_status_list.count(0) > 50:
                alarmCal = 1
                isAngrySound = 0
                isSadSound = 0

                soundAngry.stop()
                soundSad.stop()

            else:
                alarmCal = 0

            if alarmCal == 1 and sound.get_num_channels() == 0:
                set_volume(20)
                sound.play(loops=-1)

                #Uyku uyarisi calarsa butun duygulari sifirla ve duygulara ait sesleri bitir.
                listEmotion.clear()
                listEmotionEnd.clear()
                soundSad.stop()
                soundAngry.stop()

            elif alarmCal == 1:
                increase_volume(0.0005)

                #duygu listesini boşalt
                listEmotion.clear()
                listEmotionEnd.clear()


            elif alarmCal == 0 and eye_status_list.count(0) < 40:
                sound.stop()

            # Durumu yazdır
            status = "Kapali" if avg_ear < EAR_THRESHOLD else "Acik"
            cv2.putText(frame, f"Goz Durumu: {status}",       (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
            cv2.putText(frame, f"Kirpma Sayisi: {blink_count}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100,255,100), 2)

    # ——————————————
    # Duygu Analizi
    emotions = analyze_faces(frame)

    for emotion, (x, y, w_e, h_e) in emotions:
        # Yüz bölgesine dikdörtgen çiz
        cv2.rectangle(frame, (x, y), (x + w_e, y + h_e), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 0), 2)

        # Duyguları listeye ekler
        listEmotion.append(f'{emotion}')

        # Sürekli son 100 duyguyu tut
        listEmotionEnd = listEnd(listEmotion, 100)
        printListEmotion(listEmotionEnd)

        # Güncel duygu analizi
        currEmo = CurrentEmotion(listEmotionEnd, 50)
        #print(f'Güncel Duygu: {currEmo}')

        # Ses kontrolü
        if currEmo == 'angry' and isAngrySound == 0 and alarmCal == 0:
            if isSadSound == 1:
                soundSad.stop()
                isSadSound = 0
            soundAngry.play(maxtime=25000)
            isAngrySound = 1

        elif currEmo == 'sad' and isSadSound == 0 and alarmCal == 0:
            if isAngrySound == 1:
                soundAngry.stop()
                isAngrySound = 0
            soundSad.play(maxtime=25000)
            isSadSound = 1

        elif currEmo == 'neutral':
            pass
            """
            soundAngry.stop()
            isAngrySound = 0
            soundSad.stop()
            isSadSound = 0
            """

    #---- Terminale Duzgun Cikti Veren Fonksiyon ----#
    current_vol = get_current_volume()

    # 3) Duygu listesi son 100 eleman için sayılar
    angry = listEmotionEnd.count('angry')
    fear = listEmotionEnd.count('fear')
    happy = listEmotionEnd.count('happy')
    neutral = listEmotionEnd.count('neutral')
    sad = listEmotionEnd.count('sad')
    surprise = listEmotionEnd.count('surprise')
    curr_emo = CurrentEmotion(listEmotionEnd, 50)

    # 4) Konsolu tek satırda güncelle
    print_status(
        blink_count,
        eye_status_list,
        current_vol,
        curr_emo,
        (angry, fear, happy, neutral, sad, surprise)
    )
    # ---- Terminale Duzgun Cikti Veren Fonksiyon ----#


    # Pencereleri göster
    cv2.imshow("Canli Goz ve Duygu Takibi", frame)

    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()

##### MAIN (END) #####

