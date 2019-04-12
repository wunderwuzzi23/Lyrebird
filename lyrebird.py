#!/usr/bin/env python3

###############################################################################
### Lyrebird - Funky Lockscreen Fun  (alpha)
### Anyone every tried to use your computer while you step away for a second? 
### April 2019,  MIT License
###############################################################################

import time
import ctypes
import subprocess
import numpy as np
import pyscreenshot as ImageGrab
from datetime import datetime
from sys import platform
from cv2 import cv2

### flag to sync the two different input methods
Capturing = False

def Lyrebird():

   global Capturing

   ### Noticed DPI scaling is off at times on Windows
   ### If it still doesn't work correctly, right click python.exe in Explorer
   ### and set DPI compatibility as workaround under Compatibility settings
   if platform == "win32":    
      ctypes.windll.shcore.SetProcessDpiAwareness(2)
   
   ### Take a screenshot and convert it so opencv can process it
   screenshot_temp = ImageGrab.grab()
   screenshot = np.array(screenshot_temp)
   screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
 
   ### create a new fullscreen window and load the screenshot
   WindowName = "Lyrebird"
   cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
   cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
   cv2.imshow(WindowName, screenshot) 

   Capturing = True

   ### Goal is to take a picture when mouse or keyboard is clicked
   cv2.setMouseCallback(WindowName, mouseAction)

   while Capturing:
      if (cv2.waitKey(1) & 0xFF) == 27:
         webcamCapture()
         break
  
   cv2.destroyAllWindows()
  
def webcamCapture():
   camera = cv2.VideoCapture(0)
   cameraAvailable, frame = camera.read()

   if cameraAvailable:
      prefix = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
      filename = prefix + ".capture.png"
      cv2.imwrite(filename, frame)
      
      camera.release()
      print("Lyrebird - Screenshot " + filename)

   else:
      print("Lyrebird - No camera found.")


def mouseAction(event, x, y, flags, param):
   global Capturing

   if event == cv2.EVENT_LBUTTONDOWN:
      webcamCapture()
      Capturing = False

def LockWorkstation():
   print("Locking Workstation.")
   
   if platform == "win32":
      ctypes.windll.user32.LockWorkStation()
   elif platform == "darwin":
      lockMacCommand = "/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession"
      subprocess.run([lockMacCommand, "-suspend"])


if __name__ == "__main__":

   print("[root] ~ # ", end="")

   Lyrebird()
   LockWorkstation()
   print("Done.")