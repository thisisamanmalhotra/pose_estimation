#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog


def createwidgets():
    root.feedlabel = Label(root, bg="DARK GREY", fg="black", text="HUMAN POSE ESTIMATION", font=('Open Sans',20))
    root.feedlabel.grid(row=1, column=2, padx=0, pady=0, columnspan=3)
    root.cameraLabel = Label(root, bg="black", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=2, padx=10, pady=10, columnspan=3)
    root.CAMBTN = Button(root, text="STOP", command=StopCAM, bg="LIGHTBLUE", font=('Open Sans',15), width=13)
    root.CAMBTN.grid(row=4, column=3)

    ShowFeed()


def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()

    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)

        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,450), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image = videoImg)

        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        root.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')


# Defining StopCAM() to stop WEBCAM Preview
def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="START", command=StartCAM)

    # Displaying text message in the camera label
    root.cameraLabel.config(text="Click Start Button", font=('Open Sans',90))
   

def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0)

    # Setting width and height
    width_1, height_1 = 720, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP", command=StopCAM)

    # Removing text message from the camera label
    root.cameraLabel.config(text="")

    # Calling the ShowFeed() Function
    ShowFeed()

# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index
root.cap = cv2.VideoCapture(0)

# Setting width and height
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Setting the title, window size, background color and disabling the resizing property
root.title("Human pose estimation APP")
root.geometry("680x900")
root.resizable(True, True)
root.configure(background = "DARK GREY")

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

createwidgets()
root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:




