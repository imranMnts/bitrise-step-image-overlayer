from os import listdir
from os import path
from PIL import Image, ImageDraw, ImageFont
import sys

### >>> INIT <<< ###

leftIcon = None
rightIcon = None

### >>> FUNCTIONS <<< ###

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
def customizeImage(backgroundPath, leftIconPath, rightIconPath, outputPath, textColor):
  background = Image.open(backgroundPath)
  background = background.convert("RGBA")
  backgroundWidth = background.size[0]
  backgroundHeight = background.size[1]

  if path.exists(leftIconPath):
    leftIcon = Image.open(leftIconPath)
    leftIcon = leftIcon.convert("RGBA")
  else:
    leftIcon = createAnImageFromText(backgroundPath, leftIconPath, textColor)
    leftIcon = leftIcon.convert("RGBA")

  if path.exists(rightIconPath):
    rightIcon = Image.open(rightIconPath)
    rightIcon = rightIcon.convert("RGBA")
  else:
    rightIcon = createAnImageFromText(backgroundPath, rightIconPath, textColor)
    rightIcon = rightIcon.convert("RGBA")

  padding = int(background.size[0] / 20)
  if (padding > 5):
    padding = 5
  result = background.copy()
  if leftIcon != None:
    leftIcon = changeImageSizeWithRatio(background, leftIcon)
    leftIconHeight = leftIcon.size[1]
    result.paste(leftIcon, (padding, backgroundHeight - leftIconHeight - padding), leftIcon)
  if rightIcon != None:
    rightIcon = changeImageSizeWithRatio(background, rightIcon)
    rightIconWidth = rightIcon.size[0]
    rightIconHeight = rightIcon.size[1]
    result.paste(rightIcon, (backgroundWidth - rightIconWidth - padding, backgroundHeight - rightIconHeight - padding), rightIcon)
  result.save(outputPath, quality=100)


# To add icon(s) to each item (function triggered only if the source is a folder)
def findAndCustomizeImages(basepath, leftIconPath, rightIconPath, textColor):
  for fileName in listdir(basepath):
    fullPath = basepath + fileName
    if not path.exists(fullPath):
      print("!! Image not found, please check the path )")
      print("!! Path: " + fullPath)
      sys.exit(1)

    if path.isfile(fullPath) and (fullPath.endswith('.png') or fullPath.endswith('.jpg') or fullPath.endswith('.jpeg')):
      customizeImage(fullPath, leftIconPath, rightIconPath, fullPath, textColor)


# Convert the input text to image
def createAnImageFromText(backgroundPath, text, textColor):
  background = Image.open(backgroundPath)
  background = background.convert("RGBA")

  imgWidth = int(background.size[0]/2)
  imgHeight = int(background.size[1]/3)
  iconBackground = Image.new(mode="RGBA", size=(imgWidth, imgHeight), color=(0,0,0,0))

  fontsize = 1
  imgFraction = 0.50
  iconFont = ImageFont.truetype('Lato-Bold.ttf', fontsize)
  while iconFont.getsize(text)[0] < imgFraction * background.size[0]:
    # iterate until the text size is just larger than the criteria
    fontsize += 1
    iconFont = ImageFont.truetype('Lato-Bold.ttf', fontsize)

  canvas = ImageDraw.Draw(iconBackground)
  text_width, text_height = canvas.textsize(text, font=iconFont)
  x_pos = int((imgWidth - text_width) / 2)
  y_pos = int((imgHeight - text_height) / 2)

  canvas.text((x_pos, y_pos), text, font=iconFont, fill=textColor)
  return iconBackground