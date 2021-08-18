from PIL import Image, ImageFilter
import PIL.ImageOps
import numpy as np
import cv2
from random import seed
from random import randint
import glob
import time

saveFilePath = "C:\\Users\\Mikey\\OneDrive\\strawberrySam\\UptoDateFinalImages\\"
#Using Image.show() produces higher quality images vs. cv2.imread()
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
    for myFile in glob.glob(filePath + '/*.png'):
        image = Image.open(myFile).convert('RGBA')
        layer.append(image)
    newImg = layer[randint(0, len(layer) - 1)]
    #newImg.putdata(RemoveWhite(newImg.getdata()))
    return Image.alpha_composite(backgroundImg, newImg)

#This loops through the image creation and shows the images and or saves them
bodyImg = Image.open("Body/body@3x.png").convert('RGBA')

for x in range(1):
    startTime = time.time()
    backgroundImg = Image.alpha_composite(backgroundImg, bodyImg)

    backgroundImg = AddLayer("Eyes")
    backgroundImg = AddLayer("Mouths")

    backgroundImg.show()
    #backgroundImg.save(saveFilePath + str(x + 100) + '.png')

    backgroundImg = background[randint(0, len(background)) - 1]
    print("Photo " + str(x + 1) + " took " + str(time.time() - startTime), "to make.")

