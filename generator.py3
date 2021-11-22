from os import path
import sys
from . import utils

### >>> INIT <<< ###

leftIcon = None
rightIcon = None

### >>> MAIN <<< ###

if (len(sys.argv) < 2) or (not sys.argv[1]):
  print("!! Empty background (first parameter)")
  sys.exit(1)
if len(sys.argv) < 3:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)

backgroundPath = sys.argv[1]
print('backgroundPath : ', backgroundPath)
if not path.exists(backgroundPath):
  print("!! Background image not found, please check the path )")
  print("!! Path: " + backgroundPath)
  sys.exit(1)

if len(sys.argv) > 4 and len(sys.argv[4]):
  outputPath = sys.argv[4]
else:
  outputPath = backgroundPath
print('outputPath : ', outputPath)

if len(sys.argv) > 5 and len(sys.argv[5]):
  textColor = sys.argv[5]
else:
  textColor = "#FFFFFF"
print('textColor : ', textColor)

if(len(sys.argv[2])):
  leftIconPath = sys.argv[2]
  print('leftIconPath : ', leftIconPath)
if((len(sys.argv) > 3) and (len(sys.argv[3]))):
  rightIconPath = sys.argv[3]
  print('rightIconPath : ', rightIconPath)
elif not leftIconPath:
  print("!! Script required at least 2 parameters (source_image, left_icon and/or right_icon)")
  sys.exit(1)

if path.isfile(backgroundPath):
  utils.customizeImage(backgroundPath, leftIconPath, rightIconPath, outputPath, textColor)
else:
  utils.findAndCustomizeImages(backgroundPath, leftIconPath, rightIconPath, textColor)
