# BARAN KANAT - 22100011013

##### KUTUPHANELER (START) #####
import cv2
import numpy as np
import pygame.mixer
from tensorflow.keras.models import load_model
##### KUTUPHANELER (END) #####

##### DEGISKENLER (START) #####
# MODEL
model = load_model("Models/model.h5")
classes = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']
detector = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')

listEmotion = [] # Kullanicinin duygusu bu listede tutulacaktir
listEmotionEnd = [] # Kullanicinin son 100 duygusu



# Pygame ses motorunu başlat
pygame.mixer.init()
# Ses dosyasını yükle
soundAngry = pygame.mixer.Sound("Sounds/Angry.mp3") # kullanicinin sinirli oldugu durumda caliacak 'rahatlatici' muzik
soundSad = pygame.mixer.Sound("Sounds/Sad.mp3") # kullanici uzgunken calacak 'tempolu' muzik

# duygu ses kontrolleri
isAngrySound = 0 # 'rahatlatici' muzik calinip calinmadigini kontrol eder.
isSadSound = 0 # 'tempolu' muzik calinip calinmadigini kontrol eder.

##### DEGISKENLER (END) #####

##### FONKSIYONLAR (START) #####
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

    print(f'Sinirli: {angry}, Korku: {fear}, Mutlu: {happy}, Nötr: {neutral}, Üzgün: {sad}, Şaşkın: {surprise}')

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




# Kamera ile sürekli analiz
def Start():
    global isAngrySound, isSadSound
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        emotions = analyze_faces(frame)

        for emotion, (x, y, w, h) in emotions:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, emotion, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)

            #Duygulari listeye ekler
            listEmotion.append(f'{emotion}')

            #Duygu listesini olusturur
            #printListEmotion(listEmotion)

            # Surekli son 100 duyguyu yazdirir.
            listEmotionEnd = listEnd(listEmotion, 100)
            printListEmotion(listEmotionEnd)

            # Son 100 duyguya gore duygu analizi
            currEmo = CurrentEmotion(listEmotionEnd, 50)
            print(f'Güncel Duygu: {currEmo}')

            if currEmo == 'angry' and isAngrySound == 0:
                #uzgun sarki caliyorsa durdur
                if isSadSound == 1:
                    soundSad.stop()
                    isSadSound = 0

                #sinirli sarki cal
                soundAngry.play(maxtime=25000)
                isAngrySound = 1

            elif currEmo == 'sad' and isSadSound == 0:

                #sinirli sarki caliyorsa durdur
                if isAngrySound == 1:
                    soundAngry.stop()
                    isAngrySound = 0

                #uzgun sarkiyi cal
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

        cv2.imshow("Duygu Takibi", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
##### FONKSIYONLAR (END) #####


##### MAIN #####
Start()


