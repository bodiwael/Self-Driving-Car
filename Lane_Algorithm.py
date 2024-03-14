#====================== Importing Libraries ==========================
# import Carmove

from time import sleep
import serial

import cv2

import numpy as np
# from infer import main
import Action
import asyncio


cap = cv2.VideoCapture(0)
# ser = serial.Serial('COM3')  # open serial port
# print(ser.name)


def getImg(display = False , size = [480 , 240]) :
    
    _,img = cap.read()
    
    img = cv2.resize(img , (size[0] , size[1]))
    
    img = cv2.rotate(img , cv2.ROTATE_180)
    
#     if display :
        
#         cv2.imshow('IMG' , img)
        
    return img

#=======================  Declerating Functions =======================

curveList = []

avgVal = 10

def getlanecurve (img , display = 2):
    
    imgCopy = img.copy()
    
    imgResult = img.copy()
    
    imgThres = Action.thresholding(img)
 
    hT, wT, c = img.shape
     
    points = Action.valTracbars()
    
    imgWarp = Action.warpImg(imgThres , points , wT, hT)
 
    imgwarpPoints = Action.drawPoints(imgCopy , points)
    
    midllePoint , imgHist = Action.getHistogram(imgThres , display = True , minPer = 0.5 , region = 4)
    
    curveAveragePoint , imgHist = Action.getHistogram(imgThres , display = True , minPer = 0.9)
    
    curveRaw = curveAveragePoint - midllePoint
    
    curveList.append(curveRaw)
    
    if len(curveList) > avgVal :
        
        curveList.pop(0)
        
    curve = int(sum(curveList)/len(curveList))
    
    if display != 0 :
        
        imgInvWarp = Action.warpImg(imgWarp , points , wT , hT , inv = True)
        
        imgInvWarp = cv2.cvtColor(imgInvWarp , cv2.COLOR_GRAY2BGR)
        
        imgInvWarp[0:hT // 3 , 0:wT] = 0 , 0 , 0
        
        imgLaneColor = np.zeros_like(img)
        
        imgLaneColor[:] = 0 , 255 , 0
        
        imgLaneColor = cv2.bitwise_and(imgInvWarp , imgLaneColor)
        
        imgResult = cv2.addWeighted(imgResult , 1 , imgLaneColor , 1 , 0)
        
        midY = 450
        
        cv2.putText(imgResult , str(curve) , (wT // 2 - 80, 85) , cv2.FONT_HERSHEY_COMPLEX, 2 , (255,0,255),3)
        
        cv2.line(imgResult, (wT//2 , midY) , (wT // 2 + (curve*3),midY),(255,0,255),5)
        
        cv2.line(imgResult, ((wT // 2 + (curve *3)),midY-25),(wT // 2 + (curve * 3), midY + 25), (0,255,0),5)
        
        for x in range(-30,30):
            
            w = wT // 20
            
            cv2.line(imgResult , (w * x + int(curve // 50) , midY - 10),
                    (w * x + int(curve // 50) , midY + 10) , (0 , 0 , 255 ) , 2)
    
    if display == 2 :
        
        imgStacked = Action.stackImages(0.7 , ([img , imgwarpPoints, imgWarp],
                                               [imgHist, imgLaneColor , imgResult]))
        
#         cv2.imshow('ImageStack', imgStacked)
    
    elif display == 1 :
        
        cv2.imshow('Result' , imgResult)
        
    curve = curve / 100
    
    if curve > 1 : curve == 1
    
    if curve < -1 : curve == -1
        
    cv2.imshow('Edited2' , imgThres)
    
#     cv2.imshow('Edited1' , imgWarp)
    
#     cv2.imshow('Edited3' , imgwarpPoints)
    
    cv2.imshow('Edited4' , imgHist)
    
    return curve

#========================= Main Function ==========================

if __name__ == '__main__' :
    
    intialTrackBarVals = [ 101 , 0 , 0 , 100 ]
    
    Action.initializeTrackbars(intialTrackBarVals)
    
    curveList = []
    
    while True :
        
        img = getImg(True)
        
        curve = getlanecurve(img , display = 1)
        
        print(curve)
        
#         asyncio.run(main())
# #         
#         if(classes == 'stop sign'):
#              ser.write(b's')
#         
#        
#         if(classes == '120 speed limit'):
#              ser.write(b'osl')
#              
#         if(classes == 'speed bump'):
#              ser.write(b'sb')
#              
#         if(classes == '60 speed limit'):
#              ser.write(b'ssl')
#              
#         if(classes == '90 speed limit'):
#              ser.write(b'nsl')
             
        if curve > 0.65 :
            
#             Carmove.Left()
            print("Left !!")
#             ser.write(b'l')
        
        elif curve < -0.65 :
            
            print("Right !!")
#             ser.write(b'r')           
            
        else :
            
             print("Forward !!!")
#              ser.write(b'f')
                
#         cv2.imshow('Original' , img)
                
        cv2.waitKey(1)
        
        
        