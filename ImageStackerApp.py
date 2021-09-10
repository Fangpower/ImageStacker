import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from random import *
import glob
import time
#import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yagmail

BLUE = "#404040"
SUNGLOW = "#b3b3b3"
PLATINUM = "#181818"
HIGHLIGHT = "#282828"

ROSE = "#DF2935"
MINTGREEN = "#B0FF92"

FONT = ("Arial", 15, "bold")
LARGEFONT = ("Arial", 30)
FONTTWO = ("Arial", 10, "bold")
SENDER = 'fangpowerdev@gmail.com'
check = u'\u2713'

times = []
count = []

class ImageStackerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("350x640")
        self.window.resizable(0, 0)
        self.window.title("Image Stacker")
        self.window.wm_attributes('-toolwindow', 'True')

        self.imageFrame = self.createImageFrame()
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
        self.percent = self.CreatePercent()

        self.layers = []
        self.layerPaths = []
        self.backGroundPath = ""
        self.saveFilePath = ""

        self.imageCount = self.createImageCount()
        self.email = self.createEmailInput()
        self.createShowImages()
        self.createShowGraph()
        self.saveFileButton = self.createSaveFilePath()
        self.createImages = self.createCreateImages()

        self.showImages = False
        self.showGraph = False
        self.removeWhite = False

        self.allPowerfulList = [[], [], [], [], [], [], [], [], []]


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

    def createImageFrame(self):
        frame = tk.Frame(self.window, width=0, height=0, bg=PLATINUM, highlightthickness=2,
                         highlightbackground=HIGHLIGHT)
        frame.pack(side='right', fill='both', anchor='e')
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

    def ErrorWindow(self, message):
        errorWindow = tk.Tk()
        errorWindow.title('Error Message')
        errorWindow.wm_attributes('-toolwindow', 'True')
        error = tk.Label(errorWindow, text=message, bg=PLATINUM, fg=SUNGLOW, font=LARGEFONT)
        error.pack()

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
                           command=lambda: self.browseFilesRoot(button, "Root", False))
        button.pack(pady=5)
        return button

    def createPlusButton(self):
        button = tk.Button(self.rightFrame, text="Add", bg=SUNGLOW, width=8, height=4,  relief="flat",
                           command=lambda: self.findLayerCount())
        button.pack()
        button.place(relx=.5, rely=.5,anchor="center")
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
            try:
                self.layerPaths.pop(len(self.layerPaths) - 1)
            except:
                print("Could not pop")

    def createLayerInputs(self):
        button = tk.Button(self.layerFrame, text="Layer File Path", bg=SUNGLOW, width=12, font=FONTTWO, relief="flat")
        button.pack(pady=6)
        button.configure(command=lambda x = button: self.browseFiles(x,"Layer File Path", True))
        self.layers.append(button)
    # End of layer functions.

    #Parameter Functions
    def createImageCount(self):
        label = tk.Entry(self.parameterFrame, bg=SUNGLOW, font=FONTTWO, justify="center", relief="flat", width=15)
        label.pack(pady=5)
        label.insert(0, "100")
        return label

    def createEmailInput(self):
        label = tk.Entry(self.parameterFrame, bg=SUNGLOW, font=FONTTWO, justify="center", relief="flat", width=15)
        label.pack(pady=5)
        label.insert(0, "Email")
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

    def ShowGraph(self, button):
        if self.showGraph == False:
            self.showGraph = True
            button.configure(bg=MINTGREEN)
        else:
            self.showGraph = False
            button.configure(bg=ROSE)

    def createShowGraph(self):
        button = tk.Button(self.parameterFrame, bg=ROSE, text="Time Graph", relief="flat", width=12,
                font=FONTTWO, command=lambda: self.ShowGraph(button))
        button.pack(pady=5)

    def createSaveFilePath(self):
        button = tk.Button(self.parameterFrame, text="Save File Path", bg=SUNGLOW, font=FONTTWO, width=12, relief="flat",
                           command=lambda: self.browseFiles(button, "Save File Path", False))
        button.pack(pady=5)
        return button

    def Addbackground(self):
        background = self.allPowerfulList[0]
        return background[randrange(len(background))]

    def AddLayer(self, num, backgroundImg):
        layer = self.allPowerfulList[num+1]
        newImg = layer[randrange(len(layer))].resize((backgroundImg.size))
        return Image.alpha_composite(backgroundImg, newImg)

    def CreatePercent(self):
        label = tk.Label(self.rightFrame, text=U'\u2716', bg=PLATINUM, fg=SUNGLOW, font=FONT)
        label.pack(pady=15)
        return label

    def CreateList(self):
        tempList = [[], [], [], [], [], [], [], [], []]
        for myFile in glob.glob(self.backGroundPath + "/*.png"):
            image = Image.open(myFile)
            tempList[0].append(image)

        length = len(self.layerPaths)
        for x in range(length):
            for myFile in glob.glob(self.layerPaths[x] + "/*.png"):
                image = Image.open(myFile)
                tempList[x+1].append(image)

        return tempList

    def ImageCreator(self):
        times = []
        count = []
        string = self.imageCount.get()
        intEntry = int(string)
        start = time.time()

        self.allPowerfulList = self.CreateList()

        if self.showImages:
            for stuff in self.imageFrame.winfo_children():
                stuff.destroy()
            self.window.geometry("950x600")
            self.imageFrame.configure(width=600, height=600)
            img = ImageTk.PhotoImage(Image.new('RGBA', (600,600), (255, 200, 200)))
            image = tk.Label(self.imageFrame, image=img, width=600, height=600)
            image.pack()
        else:
            self.window.geometry("350x600")
            self.imageFrame.configure(width = 0)
            for stuff in self.imageFrame.winfo_children():
                stuff.destroy()
        max = intEntry
        print(self.allPowerfulList)
        for i in range(intEntry):
            startTime = time.time()
            self.percent.configure(text=str(int(((i+1)/max)*100)) + "%")
            #Add the background
            try:
                backgroundImg = self.Addbackground()
            except:
                self.ErrorWindow("Background Image Couldn't Load")
            #Add the different layers
            length = len(self.layerPaths)
            for x in range(length):
                backgroundImg = self.AddLayer(x, backgroundImg)
            #show the image
            if self.showImages:
                newImg = backgroundImg.resize((600, 600))
                imgNew = ImageTk.PhotoImage(newImg)
                image.configure(image=imgNew)
                image.photo = imgNew

            try:
                if self.saveFilePath != "":
                    backgroundImg.save(self.saveFilePath + "/" + str(i + 1) + '.png')
            except Exception as e:
                #self.ErrorWindow("Save Failed")
                print(e)

            times.append((time.time() - startTime))
            count.append(i)

            self.window.update()
            #backgroundImg.remove()
        self.percent.configure(text=U'\u2714')

        if self.showGraph == True:
            plt.plot(count, times, 'o', label="Time it Took")

            line = self.createLine(count, times)
            x_line = np.linspace(min(count), intEntry)
            y_line = line(x_line)

            plt.plot(x_line, y_line, '-', label="Average")
            plt.xlabel("Count")
            plt.ylabel("Time")
            plt.title("Image Creation Time Graph")
            plt.legend(loc='upper left')
            plt.savefig("Time-Graph.png")


        if self.email.get() != "Email":
            email = self.email.get()
            seconds = int((time.time() - start) * 100)/100
            totalTime = self.findTime(seconds)
            message = 'Image Stacker has finished stacking all ' + str(intEntry) + ' images. It took '\
                      + str(totalTime)
            if self.showGraph:
                context = yagmail.inline("Time-Graph.png")
                yag = yagmail.SMTP(SENDER).send(email, 'Finished', message, context)
            else:
                yag = yagmail.SMTP(SENDER).send(email, 'Finished', message)
        plt.show()

        total = 0
        for t in times:
            total += t
        print(total)

    def findTime(self, time):
        if time > 120:
            minutes = time / 60
            if minutes > 60:
                hours = minutes / 60
                return str(int(hours*100)/100) + " hours."
            else: return str(int(minutes*100)/100) + " minutes."
        else: return str(time) + " seconds."

    def createLine(self, x, y):
        coefs = np.polyfit(x, y, deg=8)
        line = np.poly1d(coefs)
        return line

    def createCreateImages(self):
        button = tk.Button(self.parameterFrame, text="Create Images", bg=SUNGLOW, width=12, font=FONTTWO, borderwidth=1,
                           relief="flat", command=lambda: self.ImageCreator())
        button.pack(pady=5)
        return button
    #End of parameter functions

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageStackerApp()
    app.run()