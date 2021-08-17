from PIL import Image, ImageFilter
import PIL.ImageOps
import numpy as np
import cv2
from random import seed
from random import randint
import glob

#Get the background colour image
background = []
backgroundFiles = glob.glob("Background/*.png")
for myFile in backgroundFiles:
    image = Image.open(myFile)
    background.append(image)
backgroundImg = background[randint(0, len(background)) - 1]

#This function removes all white from images to make sure they are transparent
def RemoveWhite(datas):
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    return newData

#This funtion gets the file path, and a random image, then adds it to the background image.
def AddLayer(filePath):
    layer = []
    layerFiles = glob.glob(filePath)
    for myFile in layerFiles:
        image = Image.open(myFile).convert('RGBA')
        #imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        layer.append(image)

    newImg = layer[randint(0, len(layer) - 1)]
    newImg.putdata(RemoveWhite(newImg.getdata()))
    #newImg = newImg.filter(ImageFilter.SMOOTH_MORE)
    return Image.alpha_composite(backgroundImg, newImg)

for x in range(25):
    bodyImg = Image.open("Body/PNGBODY.png").convert('RGBA')
    backgroundImg = Image.alpha_composite(backgroundImg, bodyImg)

    backgroundImg = AddLayer("Eyes/*.png")
    backgroundImg = AddLayer("Mouths/*.png")

    #backgroundImg.show()
    backgroundImg.save(str(x) + '.png')
    backgroundImg = background[randint(0, len(background)) - 1]

