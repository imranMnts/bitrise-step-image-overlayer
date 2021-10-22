from os import listdir
from os import path
from PIL import Image
import sys

# Function to change the image size
def changeImageSizeWithRatio(appIcon, overlayPath):
  appIconWidth = appIcon.size[0]
  appIconHeight = appIcon.size[1]

  overlay = Image.open(overlayPath)
  overlay = appIcon.convert("RGBA")
  overlayWidth = overlay.size[0]
  overlayHeight = overlay.size[1]

  if overlayWidth > overlayHeight:
    width = appIconWidth/2
    widthPercent = (width / float(overlayWidth))
    height = int((float(overlayHeight) * float(widthPercent)))
  else:
    height = appIconHeight/3
    heightPercent = (height / float(overlayHeight))
    width = int((float(overlayWidth) * float(heightPercent)))

  return overlay.resize((int(width), int(height)))

def customize_image(appIcon, resultIcon, leftIconPath, rightIconPath, outputPath):
  if len(leftIconPath):
    leftIcon = Image.open(leftIconPath)
    leftIcon = leftIcon.convert("RGBA")
    leftIcon = changeImageSizeWithRatio(appIcon, leftIcon)
    result.paste(leftIcon, (10, appIcon.size[1] - leftIcon.size[1] - 10), leftIcon)
  if len(rightIconPath):
    rightIcon = Image.open(rightIconPath)
    rightIcon = rightIcon.convert("RGBA")
    rightIcon = changeImageSizeWithRatio(appIcon, rightIcon)
    result.paste(rightIcon, (10, appIcon.size[1] - rightIcon.size[1] - 10), rightIcon)
  result.save(outputPath, quality=100)


def find_and_customize_images(basepath, leftIconPath, rightIconPath):
  for fileName in listdir(basepath):
    fullPath = basepath + fileName

    if path.isfile(fullPath) and (fullPath.endswith('.png') or fullPath.endswith('.jpg')):
      appIcon = Image.open(appIconPath)
      appIcon = appIcon.convert("RGBA")
      customize_image(appIcon, leftIconPath, rightIconPath)

if (not sys.argv[1]):
  print("!! Empty background (first parameter)")
  sys.exit(1)

if len(sys.argv) < 3:
  print("!! Script required at least 2 parameters (background, leftOverlay, rightOverlay)")
  print("!! Fill blank string if not needed")
  sys.exit(1)

appIconPath = sys.argv[1]
appIcon = Image.open(appIconPath)
appIcon = appIcon.convert("RGBA")

if len(sys.argv[4]):
  outputPath = sys.argv[4]
  print('outputPath : ', outputPath)
  result = appIcon.copy()
else
  

if len(outputPath):

if(len(sys.argv[2])):
  leftIconPath = sys.argv[2]
  leftIcon = Image.open(leftIconPath)
  leftIcon = leftIcon.convert("RGBA")
  leftIcon = changeImageSizeWithRatio(appIcon, leftIcon)
  result.paste(leftIcon, (10, appIcon.size[1] - leftIcon.size[1] - 10), leftIcon)

if((len(sys.argv) > 3) and (len(sys.argv[3]))):
  if (len(sys.argv[3])):
    rightIconPath = sys.argv[3]
    rightIcon = Image.open(rightIconPath)
    rightIcon = rightIcon.convert("RGBA")
    rightIcon = changeImageSizeWithRatio(appIcon, rightIcon)
    result.paste(rightIcon, (appIcon.size[0] - rightIcon.size[0] - 10, appIcon.size[1] - rightIcon.size[1] - 10), rightIcon)
  elif (not leftIconPath):
    print("!! Script required at least 2 parameters (background, leftOverlay?, rightOverlay?)")
    print("!! Fill blank strings if not needed, BUT you cannot have 2 empty strings for overlays")
    sys.exit(1)
elif not leftIconPath:
  print("!! Script required at least 2 parameters (background, leftOverlay, rightOverlay)")
  print("!! Fill blank strings if not needed, BUT you cannot have 2 empty strings for overlays")
  sys.exit(1)

if path.isfile(appIconPath):
  customize_image(appIconPath, leftIconPath, rightIconPath, outputPath)
else:
  find_and_customize_images(appIconPath, leftIconPath, rightIconPath, outputPath)
