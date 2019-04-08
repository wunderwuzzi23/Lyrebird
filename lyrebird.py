#!/usr/bin/env python3

###############################################################################
### Lyrebird - Funky Lockscreen Fun  (alpha)
### Anyone every tried to use your computer while you step away for a second?
### April 2019,  MIT License
###############################################################################

import time
import ctypes
import numpy as np
import pyscreenshot as ImageGrab
from datetime import datetime
from sys import platform
from cv2 import cv2

def Lyrebird():

   message = "Unexpected Error."

   ### take a screenshot and convert it so opencv can process it
   #ImageGrab.grab().save("test.png")
   screenshot_temp = ImageGrab.grab()
   screenshot = np.array(screenshot_temp.convert('RGB'))
 
   ### create a new fullscreen window and load the screenshot
   cv2.namedWindow("Lyrebird", cv2.WINDOW_NORMAL)
   cv2.setWindowProperty("Lyrebird", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
   cv2.imshow("Lyrebird", screenshot) 

   ### wait for the user to enter a key
   key = cv2.waitKey()

   ## did the user press ESCAPE?
   if key != 27:
   
      ### ESC was not pressed, take a screenshot
      camera = cv2.VideoCapture(0)
      cameraAvailable, frame = camera.read()

      if cameraAvailable:
         prefix = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
         filename = prefix + ".capture.png"
         cv2.imwrite(filename, frame)
         
         camera.release()
         message = "Lyrebird - Screenshot " + filename 
     
      else:
         message = "Lyrebird - No camera found."
        
   cv2.destroyAllWindows()
   message = "Lyrebird - Regular Exit."

   return message


def LockWorkstation():
   if platform == "win32":
      ctypes.windll.user32.LockWorkStation()
   elif platform == "darwin":
      ### TODO: figure out how to do this on Mac
      pass


if __name__ == "__main__":

   result = Lyrebird()
   print(result)

   print("Locking Workstation.")
   LockWorkstation()
   
   print("Done.")