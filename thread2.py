import tkinter as tk
import threading
import time
from PIL import ImageTk, Image
import random
import cv2
import numpy as np
import imutils
from tkinter import LEFT

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
    pass

def changelogo():
    path_list = ["keobuabao/keo.png", "keobuabao/bua.png", "keobuabao/bao.png"]
    bua = cv2.imread(r'keobuabao/bua.png', 0)
    second = int(lbltime.cget("text"))
    while second>0:
        path=random.choice(path_list)
        logo = ImageTk.PhotoImage(Image.open(path))
        lblLogo.configure(image=logo)
        lblLogo.image = logo
        second = int(lbltime.cget("text"))
        time.sleep(0.1)
    pass

def startFunction():
    threading.Thread(target=timecountdown, args=()).start()
    threading.Thread(target=changelogo, args=()).start()
    pass

def playagain():
    lbltime.configure(text="5")
    pass

def captureImage():
    _, frame = cap.read()
    frame = imutils.resize(frame, width=480)
    frame = cv2.flip(frame, 1)
    h , w, _ = frame.shape
   
    y = w-350
    x = 0
    crop = frame[y:h, x:200]
    image = cv2.resize(crop, (144,144))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

winform = tk.Tk()
winform.title("Keo-Bua-Bao")
winform.geometry("900x620")

# camera = MyVideoCapture(0)

def video_stream():
    # _, frame = cap.read()
    frame = imutils.resize(frame, width=480)
    frame = cv2.flip(frame, 1)
    
    h, w, _ = frame.shape
    frame = cv2.rectangle(frame, (0,int(h)), (200,int(w-350)), (255,0,0), 2)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 
    
    
# frame camera
# cap = cv2.VideoCapture(0)
frame_camera = tk.Frame(winform, highlightbackground="black", highlightthickness=2)
lmain = tk.Label(frame_camera)
lmain.pack()
# video_stream()
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
frame_result = tk.Frame(winform, padx=10, pady=10, highlightbackground="black", highlightthickness=2, width=300, height=110)
frame_result.pack(pady=10)
winform.mainloop()

