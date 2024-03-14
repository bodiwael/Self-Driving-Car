from picamera import PiCamera

from picamera.array import PiRGBArray

from time import sleep

import Camera

import cv2

def Camera_Setup() :
    
    camera = PiCamera()

    camera.rotation = 180

    camera.resolution = (480 , 240)

    camera.framerate = 30

    rawCapture = PiRGBArray(camera , size = (480 , 240))

    sleep(0.1)

    for frame in camera.capture_continuous(rawCapture , format = "bgr" , use_video_port = True) :
        
        image = frame.array

        cv2.imshow("Image" , image)

        key = cv2.waitKey(1) & 0xFF

        rawCapture.truncate(0)

        if key == ord("q"):
            
            cv2.destroyAllWindows()
            
            break

if __name__ == '__main__' :
    
    while True :
        
        Camera_Setup()