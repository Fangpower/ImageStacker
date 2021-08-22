import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *

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
        self.window.geometry("250x600")
        self.window.resizable(0, 0)
        self.window.title("Image Stacker")
        p1 = PhotoImage(file = 'body.png')
        self.window.iconphoto(False, p1)

        self.bgFileFrame = self.createBgFileFrame()
        self.layerFrame = self.createLayersFrame()
        self.parameterFrame = self.createParametersFrame()

        self.bgFileButton = self.bgFilePathInput()

        self.layers = []
        self.updateLayerCount = self.createUpdateLayerCountButton()

        self.imageCount = self.createImageCount()
        self.createRemoveWhite()
        self.createShowImages()
        self.saveFilePath = self.createSaveFilePath()
        self.createImages = self.createCreateImages()

        self.showImages = False
        self.removeWhite = False


        #All these functions are the different frames.
    def createBgFileFrame(self):
        frame = tk.Frame(self.window, width = 500, height = 25, bg=PLATINUM)
        frame.pack(expand=False, fill="both")
        return frame

    def createLayersFrame(self):
        frame = tk.Frame(self.window, width=500, height=100, bg=PLATINUMTWO)
        frame.pack(expand=True, fill="both")
        return frame

    def createParametersFrame(self):
        frame = tk.Frame(self.window, width=500, height=200, bg=PLATINUM)
        frame.pack(expand=True, fill="both")
        return frame
    #This is the end of the functions for the frames.

    #This is the function for the background file path.
    def browseFiles(self, label, filetype):
        filename = filedialog.askdirectory(initialdir = "/", title = "Select a File")
        if filename == "":
            label.configure(text=filetype)
        else:
            label.configure(text=filename)

    def bgFilePathInput(self):
        label = tk.Label(self.bgFileFrame, text="Image Stacker", font=FONT, bg=PLATINUM, fg=BLACK)
        label.pack(pady=5)
        button = tk.Button(self.bgFileFrame, text="Background File Path", bg=SUNGLOW, font=FONTTWO,
                           command=lambda: self.browseFiles(button, "Background File Path"), borderwidth=1, relief="groove")
        button.pack(pady=15)
        return button
    #End of background file path functions.

    #Start of layer functions.
    def findLayerCount(self):
        if len(self.layers) < 7:
            self.createLayerInputs()
            if len(self.layers) == 7:
                self.updateLayerCount.destroy()

    def createUpdateLayerCountButton(self):
        button = tk.Button(self.layerFrame, text="Add Layer", bg=SUNGLOW, font=FONTTWO, command=lambda: self.findLayerCount(), borderwidth=1, relief="groove")
        button.pack(pady=15)
        return button

    def createLayerInputs(self):
        button = tk.Button(self.layerFrame, text="Layer File Path", bg=SUNGLOW, font=FONTTWO, borderwidth=1, relief="groove")
        button.pack(pady=5)
        button.configure(command=lambda x = button: self.browseFiles(x, "Layer File Path"))
        self.layers.append(button)

    # End of layer functions.

    #Parameter Functions
    def createImageCount(self):
        label = tk.Entry(self.parameterFrame, bg=BLUE, font=FONTTWO, justify="center", relief="groove")
        label.pack(pady=15)
        label.insert(0, "Image Count")

    def RemoveWhite(self, button):
        if self.removeWhite == False:
            self.removeWhite = True
            button.configure(bg=MINTGREEN)
        else:
            self.removeWhite = False
            button.configure(bg=ROSE)

    def createRemoveWhite(self):
        button = tk.Button(self.parameterFrame, bg=ROSE, text="Remove White", borderwidth=1, relief="groove", font=FONTTWO, command=lambda: self.RemoveWhite(button))
        button.pack(pady=5)

    def ShowImages(self, button):
        if self.showImages == False:
            self.showImages = True
            button.configure(bg=MINTGREEN)
        else:
            self.showImages = False
            button.configure(bg=ROSE)

    def createShowImages(self):
        button = tk.Button(self.parameterFrame, bg=ROSE, text="Show Images", borderwidth=1, relief="groove", font=FONTTWO, command=lambda: self.ShowImages(button))
        button.pack(pady=5)

    def createSaveFilePath(self):
        button = tk.Button(self.parameterFrame, text="Save File Path", bg=SUNGLOW, font=FONTTWO, borderwidth=1, relief="groove",
                           command=lambda: self.browseFiles(button, "Save File Path"))
        button.pack(pady=5)
        return button

    def createCreateImages(self):
        button = tk.Button(self.parameterFrame, text="Create Images", bg=SUNGLOW, font=FONTTWO, borderwidth=1,
                           relief="groove",)
        button.pack(pady=5)
        return button
    #End of parameter functions

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageStackerApp()
    app.run()