import cv2

import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import cm
from matplotlib import colors

from tkinter import Button
from tkinter import Tk,Entry
from tkinter import filedialog as fd


def openfile():
    global filepath
    filepath= fd.askopenfilename(
                                     title="Choose the image to be processed",
                                     filetypes=(("JPEG Files","*.jpeg"), ("All files","*.*")))
    c_img = cv2.imread(filepath, 1)

    b1, g1, r1 = cv2.split(c_img)

    # Show the channels
    plt.figure(figsize=[25, 5])

    plt.subplot(141);plt.imshow(r1, cmap="gray");plt.title("Red Channel")
    plt.subplot(142);plt.imshow(g1, cmap="gray");plt.title("Green Channel")
    plt.subplot(143);plt.imshow(b1, cmap="gray");plt.title("Blue Channel")

    # Merge the individual channels into a BGR image
    imgMerged = cv2.merge((r1, g1, b1))
    # Show the merged output
    plt.subplot(144);plt.imshow(imgMerged);plt.title("Merged Output")
    plt.show()

    
def crop():  
    filepath
    c_img = cv2.imread(filepath, 1) 
    
    global cropped_region
    cropped_region = c_img[int(inp_1in.get()):int(inp_1out.get()), int(inp_2in.get()):int(inp_2out.get())]
    global b,g,r
    b,g,r = cv2.split(cropped_region)
    global cr_merg
    cr_merg = cv2.merge((r, g, b))
    

    if colourscale.get() == "b":
        plt.imshow(b, cmap="gray");plt.title("Blue channel");plt.show()
    elif colourscale.get() == "g":
        plt.imshow(g, cmap="gray");plt.title("Green Channel");plt.show()
    elif colourscale.get() == "r":
        plt.imshow(r, cmap="gray");plt.title("Red Channel");plt.show()
    elif colourscale.get() == "m":
        plt.imshow(cr_merg);plt.title("Merged Output")
        plt.show()
    elif colourscale.get() == "gr":
        cr_merg2 = cv2.cvtColor(cr_merg, cv2.COLOR_BGR2GRAY)
        plt.imshow(cr_merg2, cmap="gray");plt.title("Weighhted average Gray Output")
        plt.show()
    else:
        plt.title("Error wrong command")
        plt.show


    #show RGB Color Space
    r2, g2, b2 = cv2.split(cr_merg)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")

    pixel_colors = cr_merg.reshape((np.shape(cr_merg)[0]*np.shape(cr_merg)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    axis.scatter(r2.flatten(), g2.flatten(), b2.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.title("RGB colour space of cropped image")
    
    plt.show()


def optimummatrixval():
    if colourscale.get() == "b":
        cv2.imwrite("b crop.jpeg", b)
        print(b.max())
        print(b.min())
    elif colourscale.get() == "g":
        cv2.imwrite("g crop.jpeg", g)
        print(g.max())
        print(g.min())
    elif colourscale.get() == "r":
        cv2.imwrite("r crop.jpeg", r)
        print(r.max())
        print(r.min())
    elif colourscale.get() == "m":
        cv2.imwrite("merge(m) crop.jpeg", cr_merg)
        print(cr_merg.max())
        print(cr_merg.min())
    elif colourscale.get() == "gr":
        cr_merg2 = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("merge gray(gr) crop.jpeg", cr_merg2)
        print(cr_merg2.max())
        print(cr_merg2.min())

#creating winow and buttons
window = Tk()
window.geometry("800x500")
window.title("Program")

inp_1in = Entry(window,width=50, bg="grey", fg="white")
inp_1out= Entry(window, width=50, bg="grey", fg="white")
inp_2in = Entry(window,width=50, bg="grey", fg="white")
inp_2out= Entry(window, width=50, bg="grey", fg="white")
colourscale= Entry(window,width=75, bg="grey", fg="white")

inp_1in.insert(0,"crop in y axis index in") 
inp_1out.insert(1,"crop in y axis index out")
inp_2in.insert(2,"crop in x axis index in")
inp_2out.insert(3,"crop in x axis index out")
colourscale.insert(4,"Enter the graycolour scale required(r,g,b,merged(m), merged grayscale(gr))")

button = Button(window, text="OPEN IMAGE", command= openfile)
button.pack()

inp_1in.pack()
inp_1out.pack()
inp_2in.pack()
inp_2out.pack()
colourscale.pack()

button1 = Button(window, text="crop the image", command= crop)
button1.pack()

button2 = Button(window, text="Get optimum matrix value", command= optimummatrixval)
button2.pack()

window.mainloop()


