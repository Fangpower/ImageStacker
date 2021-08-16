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
    image = cv2.imread(myFile)
    background.append(image)
backgroundImg = Image.fromarray((background[randint(0, len(background)) - 1])).convert('RGBA')

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
        image = cv2.imread(myFile)
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        layer.append(imgRGB)
    newImg = Image.fromarray(layer[randint(0, len(layer) - 1)]).convert('RGBA')
    newImg.putdata(RemoveWhite(newImg.getdata()))
    newImg = newImg.filter(ImageFilter.SMOOTH_MORE)
    return Image.alpha_composite(backgroundImg, newImg)

for x in range(1):
    bodyImg = Image.open("Body/strawberrySam_body-1.png").convert('RGBA')
    backgroundImg = Image.alpha_composite(backgroundImg, bodyImg)

    #backgroundImg = AddLayer("Eyes/*.png")
    backgroundImg = AddLayer("Mouths/*.png")

    #backgroundImg.show()
    backgroundImg.save(str(x) + '.png')
    backgroundImg = Image.fromarray((background[randint(0, len(background)) - 1])).convert('RGBA')

