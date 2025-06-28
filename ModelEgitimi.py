# BARAN KANAT - 22100011013

### KUTUPHANELER (START) ###
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
### KUTUPHANELER (END) ###


# ----- Klasör Yolları -----
train_dir = 'veriseti/train'         # Eğitim verisi klasörü
test_dir = 'veriseti/test'     # Doğrulama verisi klasörü


# --- Parametreler ---
img_height, img_width = 48, 48
batch_size = 64
epochs = 20


# --- ImageDataGenerator ile veri hazırlığı ---
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)


# 🧠 Custom CNN Modeli
def create_custom_cnn(input_shape=(48, 48, 3), num_classes=7):
    model = Sequential()
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    # ✅ Ekstra Conv2D buraya eklenmeli
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    # ✅ Sonra Flatten ve Dense
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    return model



# ✅ Modeli oluştur ve derle

custom_model = create_custom_cnn()
custom_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# ✅ Callbacks
checkpoint = ModelCheckpoint("8-main.h5", monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
earlystop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)


# ✅ Modeli eğit
history = custom_model.fit(
    train_generator,
    epochs=epochs,
    validation_data=test_generator,
    callbacks=[checkpoint, earlystop]
)

# accuracy: 0.8824 - loss: 0.3295 - val_accuracy: 0.8529 - val_loss: 0.5130