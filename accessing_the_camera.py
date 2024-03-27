#acessing the camera
import datetime
import cv2
import numpy as np
import sys
from tkinter import *
from PIL import Image,ImageTk

#creating window
root=Tk()
root.title("Image Capture Program")
root.geometry("1000x900")
root.configure(bg="black")
Label(root,text="Webcam", font=("georgia",30,"bold"), bg="black", fg="white").pack()

#defining function
def clické():
    image = Image.fromarray(img2)
    time=str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+"_accessed_camera_program.jpg")
    image.save(time)

def close_window():
    root.destroy()

#crearing labels+frames+buttons
f1 = LabelFrame(root,bg="white")
f1.pack()

l1 = Label(f1,bg="grey")
l1.pack()

Button(root,text="save snapshot",font=("georgia",20,"bold"), bg="black", fg="black", command= clické).pack()
Button(root,text="close window",font=("georgia",20,"bold"), bg="black", fg="black", command= close_window).pack()

#passing argument in system for camera
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]
source = cv2.VideoCapture(s)

#updating the image loop with the webcam preview
while True:
    img=source.read()[1]
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img2=cv2.flip(img1, 1)
    img=ImageTk.PhotoImage(Image.fromarray(img2))
    l1['image']=img

    root.update()

source.release()





