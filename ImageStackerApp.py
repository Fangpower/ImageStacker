import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageFilter
import PIL.ImageOps
import numpy as np
import cv2
from random import seed
from random import randint
import glob
import time

BLACK = "#080708" #https://coolors.co/080708-3772ff-df2935-fdca40-e6e8e6
BLUE = "#3772FF"
ROSE = "#DF2935"
SUNGLOW = "#FDCA40"
PLATINUM = "#E6E8E6"
PLATINUMTWO = "#D6E8E6"
MINTGREEN = "#B0FF92"

FONT = ("Arial", 15, "bold")
FONTTWO = ("Arial", 10, "bold")

class ImageStackerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("350x600")
        self.window.resizable(0, 0)
        self.window.title("Image Stacker")
        p1 = PhotoImage(file = 'body.png')
        self.window.iconphoto(False, p1)

        self.leftFrame = self.createLeftFrame()
        self.rightFrame = self.createRightFrame()
        self.bgFileFrame = self.createBgFileFrame()
        self.layerFrame = self.createLayersFrame()
        self.parameterFrame = self.createParametersFrame()

        self.rootFilePath = self.createRootFileButton()
        self.plus = self.createPlusButton()
        self.minus = self.createMinusButton()
        self.bgFileButton = self.bgFilePathInput()

        self.layers = []
        #self.updateLayerCount = self.createUpdateLayerCountButton()

        self.imageCount = self.createImageCount()
        self.createShowImages()
        self.saveFilePath = self.createSaveFilePath()
        self.createImages = self.createCreateImages()

        self.showImages = False
        self.removeWhite = False


    #All these functions are the different frames.
    def createLeftFrame(self):
        frame = tk.Frame(self.window, width = 50, height = 150, bg=PLATINUM, highlightthickness=1, highlightbackground="Black")
        frame.pack(expand=True, fill="both", side="left", anchor="w")
        return frame

    def createRightFrame(self):
        frame = tk.Frame(self.window, width = 50, height = 150, bg=PLATINUM, highlightthickness=1, highlightbackground="Black")
        frame.pack(expand=True, fill="both", side="right", anchor="e")
        return frame

    def createBgFileFrame(self):
        frame = tk.Frame(self.window, width = 100, height = 25, bg=PLATINUMTWO, highlightthickness=2, highlightbackground="Black")
        frame.pack(expand=False, fill="both")
        return frame

    def createLayersFrame(self):
        frame = tk.Frame(self.window, width=100, height=100, bg=PLATINUMTWO, highlightthickness=2, highlightbackground="Black")
        frame.pack(expand=True, fill="both")
        return frame

    def createParametersFrame(self):
        frame = tk.Frame(self.window, width=100, height=15, bg=PLATINUMTWO, highlightthickness=2, highlightbackground="Black")
        frame.pack(expand=False, fill="both")
        return frame
    #This is the end of the functions for the frames.

    #This is the function for the background file path.
    def browseFiles(self, label, filetype):
        print(self.rootFilePath.cget('text'))
        filename = filedialog.askdirectory(initialdir = self.rootFilePath.cget('text'), title = "Select a File")
        if filename == "":
            label.configure(text=filetype)
        else:
            label.configure(text=filename)

    def bgFilePathInput(self):
        label = tk.Label(self.bgFileFrame, text="Image Stacker", font=FONT, bg=PLATINUMTWO, fg=BLACK)
        label.pack(pady=5)
        button = tk.Button(self.bgFileFrame, text="Background File", bg=SUNGLOW, font=FONTTWO, width=12,
                           command=lambda: self.browseFiles(button, "Background File"), borderwidth=1, relief="groove")
        button.pack(pady=15)
        return button

    #End of background file path functions.

    # Functions for side bar.
    def createRootFileButton(self):
        button = tk.Button(self.leftFrame, text="/", bg=SUNGLOW, width=8, height=4, command=lambda: self.browseFiles(button, "/"))
        button.pack(pady=5)
        return button

    def createPlusButton(self):
        button = tk.Button(self.leftFrame, text="+", bg=SUNGLOW, width=8, height=4,
                           command=lambda: self.findLayerCount())
        button.pack()
        button.place(relx=.5, rely=.5,anchor="center")
        return button

    def createMinusButton(self):
        button = tk.Button(self.leftFrame, text="-", bg=SUNGLOW, width=8, height=4,
                           command=lambda: self.removeLayerInput())
        button.pack()
        button.place(relx=.5, rely=.35, anchor="center")
        return button

    #Start of layer functions.
    def findLayerCount(self):
        if len(self.layers) < 8:
            self.createLayerInputs()

    def createUpdateLayerCountButton(self):
        button = tk.Button(self.layerFrame, text="Add Layer", bg=SUNGLOW, font=FONTTWO, width=12,
                           command=lambda: self.findLayerCount(), borderwidth=1, relief="groove")
        button.pack(pady=15)
        return button

    def removeLayerInput(self):
        if len(self.layers) > 0:
            self.layers[len(self.layers) - 1].destroy()
            self.layers.pop(len(self.layers) - 1)

    def createLayerInputs(self):
        button = tk.Button(self.layerFrame, text="Layer File Path", bg=SUNGLOW, width=12, font=FONTTWO, borderwidth=1, relief="groove")
        button.pack(pady=7)
        button.configure(command=lambda x = button: self.browseFiles(x, "Layer File Path"))
        self.layers.append(button)
    # End of layer functions.

    #Parameter Functions
    def createImageCount(self):
        label = tk.Entry(self.parameterFrame, bg=BLUE, font=FONTTWO, justify="center", relief="groove", width=15)
        label.pack(pady=15)
        label.insert(0, "1")
        return label

    def ShowImages(self, button):
        if self.showImages == False:
            self.showImages = True
            button.configure(bg=MINTGREEN)
        else:
            self.showImages = False
            button.configure(bg=ROSE)

    def createShowImages(self):
        button = tk.Button(self.parameterFrame, bg=ROSE, text="Show Images", borderwidth=1, relief="groove", width=12,
                           font=FONTTWO, command=lambda: self.ShowImages(button))
        button.pack(pady=5)

    def createSaveFilePath(self):
        button = tk.Button(self.parameterFrame, text="Save File Path", bg=SUNGLOW, font=FONTTWO, borderwidth=1, width=12, relief="groove",
                           command=lambda: self.browseFiles(button, "Save File Path"))
        button.pack(pady=5)
        return button

    def Addbackground(self):
        background = []
        backgroundFiles = glob.glob(self.bgFileButton.cget('text') + "/*.png")
        for myFile in backgroundFiles:
            image = Image.open(myFile)
            background.append(image)
        return background[randint(0, len(background)) - 1]

    def AddLayer(self, filepath, backgroundImg):
        layer = []
        for myFile in glob.glob(filepath + '/*.png'):
            image = Image.open(myFile).convert('RGBA')
            layer.append(image)
        newImg = layer[randint(0, len(layer) - 1)]
        # newImg.putdata(RemoveWhite(newImg.getdata()))
        return Image.alpha_composite(backgroundImg, newImg)

    def ImageCreator(self):
        #print(self.imageCount.get())
        string = self.imageCount.get()
        intEntry = int(string)
        for i in range(intEntry):
            #Add the background
            try:
                backgroundImg = self.Addbackground()
            except:
                print("Error")
            #Add the different layers
            for x in self.layers:
                backgroundImg = self.AddLayer(x.cget('text'), backgroundImg)
            #show the image
            if self.showImages:
                backgroundImg.show()
            if self.saveFilePath.cget('text') != "Save File Path":
                print("saved")
                try:
                    backgroundImg.save(self.saveFilePath.cget('text') + "/" + str(i + 1) + '.png')
                except TypeError as e:
                    print(i)
                    print(e)

    def createCreateImages(self):
        button = tk.Button(self.parameterFrame, text="Create Images", bg=SUNGLOW, width=12, font=FONTTWO, borderwidth=1,
                           relief="groove", command=lambda: self.ImageCreator())
        button.pack(pady=5)
        return button
    #End of parameter functions

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageStackerApp()
    app.run()