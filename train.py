import cv2
import numpy as np
import os
import random
import pickle
from imutils import paths
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten, Activation
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Input, Model
import keras

path = r'data'
num_classes =  0
for _, dirnames, _ in os.walk(path):
    num_classes += len(dirnames)
print(num_classes)

def preprocessing(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    blur = cv2.bilateralFilter(blur, 9, 75 , 75)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
    thresh = cv2.dilate(thresh, (2,2), iterations=1)
    return thresh

def savedata():
    print("[INFO] loading images...")
    data = []
    labels = []
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)

    for imagePath in imagePaths:
        #doc hinh anh
        image = cv2.imread(imagePath)
        image = preprocessing(image)
        image = cv2.resize(image, (180,180))
        # image = np.reshape(image, (128,128,1))
        data.append(image)
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)

    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    labels = to_categorical(labels)  
    print(data.shape)
    print(labels.shape)

    file = open("keobuabao.data", "wb")
    pickle.dump((data, labels), file)   
    file.close()
    return  

def loaddata():
    file = open("keobuabao.data", "rb")
    (data, labels) = pickle.load(file)
    file.close()
    return data, labels

def createModel(num_classes):
    model = Sequential()

    model.add(Conv2D(16, (3, 3), input_shape = (180,180,1), activation = 'relu', padding='same'))
    model.add(Conv2D(16, (3, 3), activation = 'relu', padding='same'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(32, (3, 3), activation = 'relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation = 'relu', padding='same'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation = 'relu', padding='same'))
    model.add(Conv2D(64, (3, 3), activation = 'relu', padding='same'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(units = 128, activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units = 16, activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units = num_classes, activation = 'softmax'))

    return model

# savedata()
data, label = loaddata()
print(data.shape)
X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.25, random_state=43)
print(X_train.shape)
model = createModel(num_classes)
model.summary()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x = X_train, y = y_train, batch_size = 64, epochs = 10, validation_data = (X_test, y_test))
model.save("modelKBB.h5")
model.evaluate(x = X_test, y= y_test, batch_size=64)