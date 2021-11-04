from os import listdir
from os import path
from PIL import Image
import sys

# Function to change the icon's size
# To adapt it to source image
def changeImageSizeWithRatio(background, overlay):
  backgroundWidth = background.size[0]
  backgroundHeight = background.size[1]

  overlayWidth = overlay.size[0]
  overlayHeight = overlay.size[1]

  if overlayWidth > overlayHeight:
    width = backgroundWidth/2
    widthPercent = (width / float(overlayWidth))
    height = int((float(overlayHeight) * float(widthPercent)))
  else:
    height = backgroundHeight/3
    heightPercent = (height / float(overlayHeight))
    width = int((float(overlayWidth) * float(heightPercent)))
  return overlay.resize((int(width), int(height)))

# Add icon(s) to the source image
def customizeImage(backgroundPath, leftIconPath, rightIconPath, outputPath):
  background = Image.open(backgroundPath)
  background = background.convert("RGBA")
  padding = int(background.size[0] / 20)
  if (padding > 10):
    padding = 10
  result = background.copy()
  if len(leftIconPath):
    leftIcon = Image.open(leftIconPath)
    leftIcon = leftIcon.convert("RGBA")
    leftIcon = changeImageSizeWithRatio(background, leftIcon)
    result.paste(leftIcon, (padding, background.size[1] - leftIcon.size[1] - padding), leftIcon)
  if len(rightIconPath):
    rightIcon = Image.open(rightIconPath)
    rightIcon = rightIcon.convert("RGBA")
    rightIcon = changeImageSizeWithRatio(background, rightIcon)
    result.paste(rightIcon, (background.size[0] - rightIcon.size[0] - padding, background.size[1] - rightIcon.size[1] - padding), rightIcon)
  result.save(outputPath, quality=100)

# To add icon(s) to each item (function triggered only if the source is a folder)
def findAndCustomizeImages(basepath, leftIconPath, rightIconPath):
  for fileName in listdir(basepath):
    fullPath = basepath + fileName
    if not path.exists(fullPath):
      print("!! Image not found, please check the path )")
      print("!! Path: " + fullPath)
      sys.exit(1)

    if path.isfile(fullPath) and (fullPath.endswith('.png') or fullPath.endswith('.jpg')):
      customizeImage(fullPath, leftIconPath, rightIconPath, fullPath)

if (len(sys.argv) < 2) or (not sys.argv[1]):
  print("!! Empty background (first parameter)")
  sys.exit(1)

if len(sys.argv) < 3:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)

backgroundPath = sys.argv[1]
if not path.exists(backgroundPath):
  print("!! Background image not found, please check the path )")
  print("!! Path: " + backgroundPath)
  sys.exit(1)

if len(sys.argv) > 4 and len(sys.argv[4]):
  outputPath = sys.argv[4]
  print('outputPath : ', outputPath)
else:
  outputPath = backgroundPath

if(len(sys.argv[2])):
  leftIconPath = sys.argv[2]
  if not path.exists(leftIconPath):
    print("!! Left icon not found, please check the path )")
    print("!! Path: " + leftIconPath)
    sys.exit(1)
else:
  leftIconPath = ""

if((len(sys.argv) > 3) and (len(sys.argv[3]))):
  rightIconPath = sys.argv[3]
  if not path.exists(rightIconPath):
    print("!! Right icon not found, please check the path )")
    print("!! Path: " + rightIconPath)
    sys.exit(1)
elif not leftIconPath:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)
else:
  rightIconPath = ""

if path.isfile(backgroundPath):
  customizeImage(backgroundPath, leftIconPath, rightIconPath, outputPath)
else:
  findAndCustomizeImages(backgroundPath, leftIconPath, rightIconPath)
