# Importing necessary libraries
import cv2

import subprocess
from PIL import Image

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
        script_path = '"$PATH"/colourdetection.py'
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
    global b1,g1,r1
    b1, g1, r1 = cv2.split(c_img)

    # Displaying each color channel and the merged image
    plt.figure(figsize=[25, 5])

    plt.subplot(141);plt.imshow(r1, cmap="gray");plt.title("Red Channel")
    plt.subplot(142);plt.imshow(g1, cmap="gray");plt.title("Green Channel")
    plt.subplot(143);plt.imshow(b1, cmap="gray");plt.title("Blue Channel")

    # Merges the individual channels into a BGR image
    global imgMerged
    imgMerged = cv2.merge((r1, g1, b1))

    plt.subplot(144);plt.imshow(imgMerged);plt.title("Merged Output")
    plt.show()


# Function to display optimum matrix values.
# As of now it is not really the best matrix value that I want, this is just a sample output of the max & min. matrix values of the image type selected.
def optimummatrixval():
    output = ""  # Initialize an empty string to store the output
    # Getting maximum and minimum matrix values based on the color scale
    if colourscale.get() == "b":
        output += f"max matrix value: {b1.max()}\nmin matrix value: {b1.min()}\n"
    elif colourscale.get() == "g":
        output += f"max matrix value: {g1.max()}\nmin matrix value: {g1.min()}\n"
    elif colourscale.get() == "r":
        output += f"max matrix value: {r1.max()}\nmin matrix value: {r1.min()}\n"
    elif colourscale.get() == "m":
        output += f"max matrix value: {imgMerged.max()}\nmin matrix value: {imgMerged.min()}\n"

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

colourscale = Entry(window, width=75, bg="grey", fg="white")
output_text = Text(window, height=2, width=50)

# Dictionary to keep track of entries and their default texts
placeholders = {
    colourscale: "Enter the graycolour scale required(r,g,b,merged(m))"
}

# Inserts the placeholder text and binds the focus_in and focus_out events
for entry, text in placeholders.items():
    entry.insert(0, text)
    entry.bind("<FocusIn>", on_entry_click)
    entry.bind("<FocusOut>", on_focusout)

# Defines the buttons
button0 = Button(window, text="Take a camera shot of the colour Blue", command=access_camera)
button = Button(window, text="OPEN IMAGE", command=openfile)
button2 = Button(window, text="Get optimum matrix value", command=optimummatrixval)
close_button = Button(window, text="Close All Windows", command=close_all_windows)

# Packs the widgets
button0.pack()
button.pack()
button2.pack()

colourscale.pack()
output_text.pack()
close_button.pack()

window.mainloop()
