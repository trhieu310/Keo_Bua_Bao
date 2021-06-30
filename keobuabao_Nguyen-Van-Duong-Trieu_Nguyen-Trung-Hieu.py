    import tkinter as tk
import threading
import time
from PIL import ImageTk, Image
import random
import cv2
import numpy as np
from tkinter import LEFT
from tensorflow.python.keras.models import load_model

rs = ["Khong co ket qua", "Keo", "Bua", "Bao"]
model = load_model("modelKBB.h5")

def getReultFromImage(model, image):
    image = preprocessing(image)
    pre = prediction(model, image)
    return np.argmax(pre)


def preprocessing(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    blur = cv2.bilateralFilter(blur, 9, 75 , 75)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
    thresh = cv2.dilate(thresh, (2,2), iterations=1)

    return thresh

def prediction(model, image):
    image = cv2.resize(image, (128,128))
    image = np.reshape(image, (1, 128,128, 1))
    image = image/255.0
    pre = model.predict(image)
    return pre

def timecountdown():
    second = int(lbltime.cget("text"))
    while second>0:
        time.sleep(1)
        second=second-1
        lbltime.configure(text=second)
    image = captureImage()
    img = ImageTk.PhotoImage(Image.fromarray(image))
    lblImage.configure(image=img)
    lblImage.image = img

    result = getReultFromImage(model, image)
    print(str(rs[result]))
    lbllogo = str(lrl.get())
    print(lbllogo)
    lblimage = str(result)
    getReult(lblimage, lbllogo)
    pass

def changelogo():
    path_list = [("keobuabao/keo.png",1), ("keobuabao/bua.png",2), ("keobuabao/bao.png",3)]
    second = int(lbltime.cget("text"))
    while second>0:
        path=random.choice(path_list)
        lrl.set(path[1])
        logo = ImageTk.PhotoImage(Image.open(path[0]))
        lblLogo.configure(image=logo)
        lblLogo.image = logo
        time.sleep(0.1)
        second = int(lbltime.cget("text"))
    pass

def startFunction():
    t1 = threading.Thread(target=timecountdown, args=())
    t1.start()
    t2 = threading.Thread(target=changelogo, args=())
    t2.start()
    
    pass

def playagain():
    lbltime.configure(text="5")
    pass

def captureImage():
    _, frame = cap.read()
    print(frame.shape)
    # frame = imutils.resize(frame, width=480)
    frame = cv2.flip(frame, 1)
    h , w, _ = frame.shape
    y = 160
    x = 0
    crop = frame[y:h, x:200]
    image = cv2.resize(crop, (144,144))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def getReult(image, logo):
    kq = lblResult.cget("text")
    if (image!= "") and (logo != ""):
        if (int(image) == int(logo)):
            kq = "Hoa roi!"
            print("hoa")
        else:
            if (int(image)==0):
                kq = "Khong co ket qua"
                print("Ko co ket qua")
            else:
                if (int(image)==1):
                    if (int(logo)==2):
                        kq= "Ban thua roi! Thu lai nhe..."
                        print("Thua")
                    else:
                        kq = "Tuyet voi! Ban da thang"
                        print("Thang")
                elif (int(image)==2):
                    if (int(logo)==3):
                        kq= "Ban thua roi! Thu lai nhe..."
                        print("Thua")
                    else:
                        kq = "Tuyet voi! Ban da thang"
                        print("Thang")
                elif (int(image)==3):
                    if (int(logo)==1):
                        kq= "Ban thua roi! Thu lai nhe..."
                        print("Thua")
                    else:
                        kq = "Tuyet voi! Ban da thang"
                        print("Thang")
    lblResult.configure(text=kq)


def video_stream():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame = cv2.rectangle(frame, (0,160), (200,int(h)), (255,0,0), 2)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 
    
    
# frame camera
cap = cv2.VideoCapture(0)
cap.set(3, 288)
cap.set(4, 384)

winform = tk.Tk()
winform.title("Keo-Bua-Bao")
winform.geometry("900x620+400+50")
frame_camera = tk.Frame(winform,width= cap.get(4), height=cap.get(3) ,highlightbackground="black", highlightthickness=2)
lmain = tk.Label(frame_camera)
lmain.pack()
video_stream()
frame_camera.pack(pady=20)

#label dem
lbltime = tk.Label(text="5", font=(15))
lbltime.pack()

#frame button start and replay
frame_start_playagain = tk.Frame(winform)
frame_start_playagain.pack()
btnStart = tk.Button(
    frame_start_playagain,
    text="Start..",
    width=10,
    padx=10,
    pady=5,
    command=lambda:startFunction()
)
btnStart.pack(side=LEFT, padx=10)

btnPlayAgain = tk.Button(
    frame_start_playagain,
    text="Play again",
    width=10,
    padx=10,
    pady=5,
    command=lambda:playagain()
)
btnPlayAgain.pack(side=LEFT, padx=10)

#Frame may ra keo bua bao
frame = tk.Frame(winform, padx=10, pady=10, highlightbackground="black", highlightthickness=2, width=144, height=144)
logo = ImageTk.PhotoImage(Image.open("keobuabao/keo.png"))
lblLogo = tk.Label(frame, image=logo)
lblLogo.pack()
frame.place(x=670, y = 420)

#Frame nguoi ra keo bua bao
frame_person = tk.Frame(winform, padx=10, pady=10, highlightbackground="black", highlightthickness=2, width=144, height=144)
logo_image = ImageTk.PhotoImage(Image.open("keobuabao/noimage.jpg"))
lblImage = tk.Label(frame_person, image=logo_image)
lblImage.pack()
frame_person.place(x=56, y = 420)

#Frame ket qua
frame_result = tk.Frame(winform, padx=10, pady=10)
lblKQ = tk.Label(frame_result, text="Result", font=(25), pady=10)
lblKQ.pack()
lblResult = tk.Label(frame_result, text="...", font=(25), pady=2)
lblResult.pack()
frame_result.pack(pady=10)

lrl = tk.StringVar()
lrl.set("")
lblResultLogo = tk.Label(winform, textvariable=lrl).pack_forget()

winform.mainloop()

