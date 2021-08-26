import tkinter as tk
from tkinter import filedialog
from tkinter import *
#from tkinter.ttk import *
from PIL import Image
#import PIL.ImageOps
#import numpy as np
#import cv2
#from random import seed
from random import randint
import glob
#import time

BLUE = "#404040"
SUNGLOW = "#b3b3b3"
PLATINUM = "#181818"
HIGHLIGHT = "#282828"

ROSE = "#DF2935"
MINTGREEN = "#B0FF92"

FONT = ("Arial", 15, "bold")
LARGEFONT = ("Arial", 30)
FONTTWO = ("Arial", 10, "bold")

class ImageStackerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("350x600")
        self.window.resizable(0, 0)
        self.window.title("Image Stacker")

        self.leftFrame = self.createLeftFrame()
        self.rightFrame = self.createRightFrame()
        self.bgFileFrame = self.createBgFileFrame()
        self.layerFrame = self.createLayersFrame()
        self.parameterFrame = self.createParametersFrame()

        self.createRootFileButton()
        self.rootFilePath = "/"
        self.plus = self.createPlusButton()
        self.minus = self.createMinusButton()
        self.bgFileButton = self.bgFilePathInput()

        self.layers = []
        self.layerPaths = []
        self.backGroundPath = ""
        self.saveFilePath = ""
        #self.updateLayerCount = self.createUpdateLayerCountButton()

        self.imageCount = self.createImageCount()
        self.createShowImages()
        self.saveFileButton = self.createSaveFilePath()
        self.createImages = self.createCreateImages()

        self.showImages = False
        self.removeWhite = False


    #All these functions are the different frames.
    def createLeftFrame(self):
        frame = tk.Frame(self.window, width = 50, height = 150, bg=PLATINUM, highlightthickness=1, highlightbackground=HIGHLIGHT)
        frame.pack(expand=True, fill="both", side="left", anchor="w")
        return frame

    def createRightFrame(self):
        frame = tk.Frame(self.window, width = 50, height = 150, bg=PLATINUM, highlightthickness=1, highlightbackground=HIGHLIGHT)
        frame.pack(expand=True, fill="both", side="right", anchor="e")
        return frame

    def createBgFileFrame(self):
        frame = tk.Frame(self.window, width = 100, height = 25, bg=PLATINUM, highlightthickness=2, highlightbackground=HIGHLIGHT)
        frame.pack(expand=False, fill="both")
        return frame

    def createLayersFrame(self):
        frame = tk.Frame(self.window, width=100, height=100, bg=PLATINUM, highlightthickness=2, highlightbackground=HIGHLIGHT)
        frame.pack(expand=True, fill="both")
        return frame

    def createParametersFrame(self):
        frame = tk.Frame(self.window, width=100, height=15, bg=PLATINUM, highlightthickness=2, highlightbackground=HIGHLIGHT)
        frame.pack(expand=False, fill="both")
        return frame
    #This is the end of the functions for the frames.

    def LabelLayerButton(self, button, filepath):
        #This loops through all the buttons in order to store their file path at the correct spot in the filepath list
        x=0
        for i in self.layers:
            #print("2")
            if i == button:
                try:
                    self.layerPaths.pop(x)
                except:
                    print("Could Not Pop")
                self.layerPaths.insert(x, filepath)
            x +=1

    def CreateSimplifiedName(self, filename):
        list = filename.split("/")
        return list[len(list) - 1]

    #This is the function for the background file path.
    def browseFiles(self, button, filetype, isLayerButton):
        filename = filedialog.askdirectory(initialdir = self.rootFilePath, title = "Select a File")
        if filename == "":
            button.configure(text=filetype)
        else:
            if button.cget('text') == "Background File":
                self.backGroundPath = filename
            elif button.cget('text') == "Save File Path":
                self.saveFilePath = filename
            button.configure(text=self.CreateSimplifiedName(filename))
            if isLayerButton:
                self.LabelLayerButton(button, filename)

    def browseFilesRoot(self, button, filetype, isLayerButton):
        filename = filedialog.askdirectory(initialdir = self.rootFilePath, title = "Select a File")
        if filename == "":
            button.configure(text=filetype)
            self.rootFilePath = "/"
        else:
            button.configure(text=self.CreateSimplifiedName(filename))
            self.rootFilePath = filename

    def bgFilePathInput(self):
        label = tk.Label(self.bgFileFrame, text="Image Stacker", font=FONT, bg=PLATINUM, fg=SUNGLOW)
        label.pack(pady=5)
        button = tk.Button(self.bgFileFrame, text="Background File", bg=SUNGLOW, font=FONTTWO, width=12,
                           command=lambda: self.browseFiles(button, "Background File", False), relief="flat")
        button.pack(pady=15)
        return button

    #End of background file path functions.

    # Functions for side bar.
    def createRootFileButton(self):
        button = tk.Button(self.leftFrame, text="Root", bg=SUNGLOW, width=8, height=4,  relief="flat",
                           command=lambda: self.browseFilesRoot(button, "/", False))
        button.pack(pady=5)
        return button

    def createPlusButton(self):
        button = tk.Button(self.leftFrame, text="Add", bg=SUNGLOW, width=8, height=4,  relief="flat",
                           command=lambda: self.findLayerCount())
        button.pack()
        button.place(relx=.5, rely=.35,anchor="center")
        return button

    def createMinusButton(self):
        button = tk.Button(self.leftFrame, text="Remove", bg=SUNGLOW, width=8, height=4, relief="flat",
                           command=lambda: self.removeLayerInput())
        button.pack()
        button.place(relx=.5, rely=.5, anchor="center")
        return button

    #Start of layer functions.
    def findLayerCount(self):
        if len(self.layers) < 8:
            self.createLayerInputs()

    def removeLayerInput(self):
        if len(self.layers) > 0:
            self.layers[len(self.layers) - 1].destroy()
            self.layers.pop(len(self.layers) - 1)

    def createLayerInputs(self):
        button = tk.Button(self.layerFrame, text="Layer File Path", bg=SUNGLOW, width=12, font=FONTTWO, relief="flat")
        button.pack(pady=6)
        button.configure(command=lambda x = button: self.browseFiles(x,"Layer File Path", True))
        self.layers.append(button)
    # End of layer functions.

    #Parameter Functions
    def createImageCount(self):
        label = tk.Entry(self.parameterFrame, bg=SUNGLOW, font=FONTTWO, justify="center", relief="flat", width=15)
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
        button = tk.Button(self.parameterFrame, bg=ROSE, text="Show Images", relief="flat", width=12,
                           font=FONTTWO, command=lambda: self.ShowImages(button))
        button.pack(pady=5)

    def createSaveFilePath(self):
        button = tk.Button(self.parameterFrame, text="Save File Path", bg=SUNGLOW, font=FONTTWO, width=12, relief="flat",
                           command=lambda: self.browseFiles(button, "Save File Path", False))
        button.pack(pady=5)
        return button

    def Addbackground(self):
        background = []
        backgroundFiles = glob.glob(self.backGroundPath + "/*.png")
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
                print("Background Failed")
            #Add the different layers
            for x in self.layerPaths:
                backgroundImg = self.AddLayer(x, backgroundImg)
            #show the image
            if self.showImages:
                backgroundImg.show()
            try:
                if self.saveFilePath != "":
                    print("saved")
                    try:
                        backgroundImg.save(self.saveFilePath + "/" + str(i + 1) + '.png')
                    except TypeError as e:
                        print(i)
                        print(e)
            except:
                print("Save Failed")

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