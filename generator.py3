from os import path
from os import listdir
import sys
from PIL import Image, ImageDraw, ImageFont

### >>> INIT <<< ###

class Variables(object):
  textContainerHeight = 0
  leftIcon = None
  rightIcon = None
  imgFraction = 0.5

### >>> FUNCTIONS <<< ###

# Function to change the icon's size
# To adapt it to source image
def changeImageSizeWithRatio(background: Image, overlay: Image, isLeftIcon: bool):
  backgroundWidth = background.size[0]
  backgroundHeight = background.size[1]

  overlayWidth = overlay.size[0]
  overlayHeight = overlay.size[1]

  if (isLeftIcon):
    fraction = Variables.imgFraction
  else:
    fraction = 0.33

  if overlayWidth > overlayHeight:
    width = backgroundWidth * fraction
    widthPercent = (width / float(overlayWidth))
    height = int((float(overlayHeight) * float(widthPercent)))
  else:
    height = backgroundHeight * fraction
    heightPercent = (height / float(overlayHeight))
    width = int((float(overlayWidth) * float(heightPercent)))
  return overlay.resize((int(width), int(height)))

# Add icon(s) to the source image
def customizeImage(backgroundPath: str, leftIconPath: str, rightIconPath: str, outputPath: str, textColor: str, centerIcon: bool):
  background = Image.open(backgroundPath)
  background = background.convert("RGBA")
  backgroundWidth = background.size[0]
  backgroundHeight = background.size[1]

  if path.exists(leftIconPath):
    Variables.leftIcon = Image.open(leftIconPath)
    Variables.leftIcon = Variables.leftIcon.convert("RGBA")
  else:
    Variables.leftIcon = createAnImageFromText(backgroundPath, leftIconPath, textColor, centerIcon)
    Variables.leftIcon = Variables.leftIcon.convert("RGBA")

  if path.exists(rightIconPath):
    Variables.rightIcon = Image.open(rightIconPath)
    Variables.rightIcon = Variables.rightIcon.convert("RGBA")
  else:
    Variables.rightIcon = createAnImageFromText(backgroundPath, rightIconPath, textColor, centerIcon)
    Variables.rightIcon = Variables.rightIcon.convert("RGBA")

  result = background.copy()
  if Variables.leftIcon != None:
    Variables.leftIcon = changeImageSizeWithRatio(background, Variables.leftIcon, True)
    leftIconWidth = Variables.leftIcon.size[0]
    leftIconHeight = Variables.leftIcon.size[1]
    x = getXPosition(backgroundWidth, leftIconWidth, True, centerIcon)
    y = getYPosition(backgroundHeight, leftIconHeight, True, centerIcon)
    result.paste(Variables.leftIcon, (x, y), Variables.leftIcon)
  if Variables.rightIcon != None:
    Variables.rightIcon = changeImageSizeWithRatio(background, Variables.rightIcon, False)
    rightIconWidth = Variables.rightIcon.size[0]
    rightIconHeight = Variables.rightIcon.size[1]
    x = getXPosition(backgroundWidth, rightIconWidth, False, centerIcon)
    y = getYPosition(backgroundHeight, rightIconHeight, False, centerIcon)
    result.paste(Variables.rightIcon, (x, y), Variables.rightIcon)
  result.save(outputPath, quality=100)


# To add icon(s) to each item (function triggered only if the source is a folder)
def findAndCustomizeImages(basepath: str, leftIconPath: str, rightIconPath: str, textColor: str, centerIcon: bool):
  for fileName in listdir(basepath):
    fullPath = basepath + fileName
    if not path.exists(fullPath):
      print("!! Image not found, please check the path )")
      print("!! Path: " + fullPath)
      sys.exit(1)

    if path.isfile(fullPath) and (fullPath.endswith('.png') or fullPath.endswith('.jpg') or fullPath.endswith('.jpeg')):
      customizeImage(fullPath, leftIconPath, rightIconPath, fullPath, textColor, centerIcon)


# Convert the input text to image
def createAnImageFromText(backgroundPath: str, text: str, textColor: str, centerIcon: bool):
  background = Image.open(backgroundPath)
  background = background.convert("RGBA")
  backgroundWidth = background.size[0]
  backgroundHeight = background.size[1]

  fontsize = 1
  txtFraction = Variables.imgFraction - 0.02
  iconFont = ImageFont.truetype(stepRootPath + "/Arial-Bold.ttf", fontsize)
  while iconFont.getsize(text)[0] < (txtFraction * backgroundWidth):
    # iterate until the text size is just larger than the criteria
    fontsize += 1
    iconFont = ImageFont.truetype(stepRootPath + "/Arial-Bold.ttf", fontsize)

  Variables.textContainerHeight = iconFont.getsize(text)[1]

  if (centerIcon):
    iconBackgroundColor=(192, 192, 192, 120)
    txtImageWidth = backgroundWidth
    txtImageHeight = backgroundHeight
  else:
    iconBackgroundColor=(0, 0, 0, 0)
    txtImageWidth = iconFont.getsize(text)[0]
    txtImageHeight = Variables.textContainerHeight

  iconBackground = Image.new(mode="RGBA", size=(txtImageWidth, txtImageHeight), color=iconBackgroundColor)

  textContainer = ImageDraw.Draw(iconBackground)
  # text_width, text_height = textContainer.textsize(text, font=iconFont)
  
  x_pos = int((txtImageWidth - iconFont.getsize(text)[0])/2)
  y_pos = int((txtImageHeight - iconFont.getsize(text)[1])/2)

  textContainer.text((x_pos, y_pos), text, font=iconFont, fill=textColor)
  return iconBackground

# Helpers
def getXPosition(backgroundWidth: int, iconWidth: int, isLeftIcon: bool, centerIcon: bool):
  if (isLeftIcon == True):
    if (centerIcon):
      return int(backgroundWidth/ 2 - iconWidth/ 2)
    else:
      return int((backgroundWidth/ 2 - iconWidth)/ 2)
  else:
    if (centerIcon == True):
      return int(backgroundWidth/ 2)
    else:
      return int(backgroundWidth/ 2 + (backgroundWidth/ 2 - iconWidth) / 2)

def getYPosition(backgroundHeight: int, iconHeight: int, isLeftIcon: bool, centerIcon: bool):
  if (centerIcon):
    if (isLeftIcon):
      return int(backgroundHeight/2 - iconHeight/ 2)
    else:
      if path.exists(leftIconPath):
        return int(backgroundHeight/2)
      else:
        # if we display a text, to not hide it
        return int(backgroundHeight/2 + (int(Variables.textContainerHeight * Variables.imgFraction))/ 2)
  else:
    return int(backgroundHeight - iconHeight - backgroundHeight/10)


### >>>> MAIN <<<< ###

if (len(sys.argv) < 3) or (not sys.argv[2]):
  print("!! Empty background (first parameter)")
  sys.exit(1)
if len(sys.argv) < 4:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)


print("List Dir: ")
print(listdir('.'))
stepRootPath = sys.argv[1]
backgroundPath = sys.argv[2]
print('backgroundPath : ', backgroundPath)
if not path.exists(backgroundPath):
  print("!! Background image not found, please check the path )")
  print("!! Path: " + backgroundPath)
  sys.exit(1)

if len(sys.argv) > 5 and len(sys.argv[5]):
  outputPath = sys.argv[5]
else:
  outputPath = backgroundPath
print('outputPath : ', outputPath)

if len(sys.argv) > 6 and len(sys.argv[6]):
  textColor = sys.argv[6]
else:
  textColor = "#FFFFFF"
print('textColor : ', textColor)

if len(sys.argv) > 7 and len(sys.argv[7]):
  centerIcon = sys.argv[7] == "True"
else:
  centerIcon = False
print('centerIcon : ', centerIcon)
if (centerIcon):
  Variables.imgFraction = 0.6

if(len(sys.argv[3])):
  leftIconPath = sys.argv[3]
  print('leftIconPath : ', leftIconPath)
if((len(sys.argv) > 4) and (len(sys.argv[4]))):
  rightIconPath = sys.argv[4]
  print('rightIconPath : ', rightIconPath)
elif not leftIconPath:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)

if path.isfile(backgroundPath):
  customizeImage(backgroundPath, leftIconPath, rightIconPath, outputPath, textColor, centerIcon)
else:
  findAndCustomizeImages(backgroundPath, leftIconPath, rightIconPath, textColor, centerIcon)
