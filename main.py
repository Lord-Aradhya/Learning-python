# Importing necessary libraries
import cv2

import subprocess

import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import cm
from matplotlib import colors

from tkinter import Button
from tkinter import Tk,Entry,Text
from tkinter import filedialog as fd

#runs the file: acessing_the_camera.py 
def access_camera():
        # Path to the script
        script_path = '/Users/macbook/Documents/coding started/opencvproject/acessing_the_camera.py'
        # Executing the script using subprocess
        subprocess.run(['python', script_path])


# Function to open a file dialog and read an image
def openfile():
    global filepath
    # Opening a file dialog to choose an image file
    filepath= fd.askopenfilename(
                                     title="Choose the image to be processed",
                                     filetypes=(("JPEG Files","*.jpeg"), ("All files","*.*")))
    # Reading the selected image
    c_img = cv2.imread(filepath, 1)

    # Splitting the image into its color channels
    b1, g1, r1 = cv2.split(c_img)

    # Displaying each color channel and the merged image
    plt.figure(figsize=[25, 5])

    plt.subplot(141);plt.imshow(r1, cmap="gray");plt.title("Red Channel")
    plt.subplot(142);plt.imshow(g1, cmap="gray");plt.title("Green Channel")
    plt.subplot(143);plt.imshow(b1, cmap="gray");plt.title("Blue Channel")

    # Merges the individual channels into a BGR image
    imgMerged = cv2.merge((r1, g1, b1))
    
    plt.subplot(144);plt.imshow(imgMerged);plt.title("Merged Output")
    plt.show()


#declares the crop function to select a particular region of interest in an image.
def crop():  
    
    c_img = cv2.imread(filepath, 1) 
    
    global cropped_region
    # Cropping the image
    cropped_region = c_img[int(inp_1in.get()):int(inp_1out.get()), int(inp_2in.get()):int(inp_2out.get())]
    global b,g,r
    b,g,r = cv2.split(cropped_region)
    global cr_merg
    cr_merg = cv2.merge((r, g, b))
    
    # Displaying the cropped image in different color scales based on user input
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
        plt.show()


    # Displaying the RGB color space of the cropped image
    # Just an extra detail since I found this interesting
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
    plt.title("colour space of cropped image")
    
    plt.show()

# Function to save the cropped image
def save_cropped_img():
    # Saving the image based on the selected color scale
    if colourscale.get() == "b":
        cv2.imwrite("b crop.jpeg", b)
    elif colourscale.get() == "g":
        cv2.imwrite("g crop.jpeg", g)
    elif colourscale.get() == "r":
        cv2.imwrite("r crop.jpeg", r)
    elif colourscale.get() == "m":
        cv2.imwrite("merge(m) crop.jpeg", cr_merg)
    elif colourscale.get() == "gr":
        cr_merg2 = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("merge gray(gr) crop.jpeg", cr_merg2)

# Function to display optimum matrix values.
# As of now it is not really the best matrix value that I want, this is just a sample output of the max & min. matrix values of the image type selected.
def optimummatrixval():
    output = ""  # Initialize an empty string to store the output
    # Getting maximum and minimum matrix values based on the color scale
    if colourscale.get() == "b":
        output += f"max matrix value: {b.max()}\nmin matrix value: {b.min()}\n"
    elif colourscale.get() == "g":
        output += f"max matrix value: {g.max()}\nmin matrix value: {g.min()}\n"
    elif colourscale.get() == "r":
        output += f"max matrix value: {r.max()}\nmin matrix value: {r.min()}\n"
    elif colourscale.get() == "m":
        output += f"max matrix value: {cr_merg.max()}\nmin matrix value: {cr_merg.min()}\n"
    elif colourscale.get() == "gr":
        cr_merg2 = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
        output += f"max matrix value: {cr_merg2.max()}\nmin matrix value: {cr_merg2.min()}\n"

    # Insert the output in the Text widget
    output_text.delete("1.0", "end")  # Clear existing text
    output_text.insert("1.0", output)  # Insert new text

def close_all_windows():
    # Closes all OpenCV windows
    window.destroy()
    # Closes all Matplotlib plot windows
    plt.close('all')

def on_entry_click(event):
    """Function to clear the placeholder text when clicking on the entry."""
    entry = event.widget
    if entry.get() == placeholders[entry]:
        entry.delete(0, "end")
        entry.config(fg='white')


def on_focusout(event):
    """Function to add the placeholder text if nothing is entered in the entry."""
    entry = event.widget
    if entry.get() == '':
        placeholder_text = placeholders[entry]
        entry.insert(0, placeholder_text)
        entry.config(fg='white')


#creating buttons and windows in tinkter
window = Tk()
window.geometry("800x500")
window.title("Program")

# Defines the Entry widgets
inp_1in = Entry(window, width=50, bg="grey", fg="white")
inp_1out = Entry(window, width=50, bg="grey", fg="white")
inp_2in = Entry(window, width=50, bg="grey", fg="white")
inp_2out = Entry(window, width=50, bg="grey", fg="white")
colourscale = Entry(window, width=75, bg="grey", fg="white")
output_text = Text(window, height=2, width=50)

# Dictionary to keep track of entries and their default texts
placeholders = {
    inp_1in: "crop in y axis index in",
    inp_1out: "crop in y axis index out",
    inp_2in: "crop in x axis index in",
    inp_2out: "crop in x axis index out",
    colourscale: "Enter the graycolour scale required(r,g,b,merged(m), merged grayscale(gr))"
}

# Inserts the placeholder text and binds the focus_in and focus_out events
for entry, text in placeholders.items():
    entry.insert(0, text)
    entry.bind("<FocusIn>", on_entry_click)
    entry.bind("<FocusOut>", on_focusout)

# Defines the buttons
button0 = Button(window, text="take a camera shot", command=access_camera)
button = Button(window, text="OPEN IMAGE", command=openfile)
button1 = Button(window, text="crop the image", command=crop)
button2 = Button(window, text="Get optimum matrix value", command=optimummatrixval)
button3 = Button(window, text="save cropped image", command=save_cropped_img)
close_button = Button(window, text="Close All Windows", command=close_all_windows)

# Packs the widgets
button0.pack()
button.pack()
button1.pack()
button2.pack()
button3.pack()

inp_1in.pack()
inp_1out.pack()
inp_2in.pack()
inp_2out.pack()
colourscale.pack()
output_text.pack()
close_button.pack()

window.mainloop()
