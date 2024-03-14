#=========================== importing libraries ================================

import cv2 as cv

import numpy as np

import RPi.GPIO as GPIO  # Respberry Pi Library

from time import sleep         # Delay library

from picamera import PiCamera         # Camera Library

#=========================== Car pin setup =======================================

initialvalue = 28 # Between 0 and 100 ( Csn be edited )

GPIO.setwarnings(False) 

GPIO.setmode(GPIO.BCM)   # BCM mode not Board mode

led = 22

Trig = 17

Echo = 27

in1 = 21  

in2 = 20  

in3 = 13

in4 = 19

En1 = 12

En2 = 26

GPIO.setup(led , GPIO.OUT)

GPIO.setup(in1 , GPIO.OUT)

GPIO.setup(in2 , GPIO.OUT)

GPIO.setup(in3 , GPIO.OUT)

GPIO.setup(in4 , GPIO.OUT)

GPIO.setup(En1 , GPIO.OUT)

GPIO.setup(En2 , GPIO.OUT)

GPIO.setup(Trig , GPIO.OUT)

GPIO.setup(Echo , GPIO.IN)

GPIO.output(in1 , GPIO.LOW)

GPIO.output(in2 , GPIO.LOW)

GPIO.output(in3 , GPIO.LOW)

GPIO.output(in4 , GPIO.LOW)

Rspeed = GPIO.PWM(En1 , 1000)

Lspeed = GPIO.PWM(En2 , 1000)

Rspeed.start(initialvalue)

Lspeed.start(initialvalue)


GPIO.output(in1 , GPIO.HIGH)
        
GPIO.output(in2 , GPIO.HIGH)
        
GPIO.output(in3 , GPIO.HIGH)
        
GPIO.output(in4 , GPIO.HIGH)

def Forward () :
    

    GPIO.output(in1 , GPIO.LOW)
            
    GPIO.output(in2 , GPIO.HIGH)
            
    GPIO.output(in3 , GPIO.HIGH)
            
    GPIO.output(in4 , GPIO.LOW)

def Backward () :
    

    GPIO.output(in2 , GPIO.LOW)
            
    GPIO.output(in1 , GPIO.HIGH)
            
    GPIO.output(in4 , GPIO.HIGH)
            
    GPIO.output(in3 , GPIO.LOW)
    
def Right () :
    
    Rspeed.start(40)

    Lspeed.start(40)

    GPIO.output(in1 , GPIO.HIGH)
            
    GPIO.output(in2 , GPIO.HIGH)
            
    GPIO.output(in3 , GPIO.HIGH)
            
    GPIO.output(in4 , GPIO.LOW)
    
def Left () :
    
    Rspeed.start(40)

    Lspeed.start(40)

    GPIO.output(in1 , GPIO.LOW)
            
    GPIO.output(in2 , GPIO.HIGH)
            
    GPIO.output(in3 , GPIO.HIGH)
            
    GPIO.output(in4 , GPIO.HIGH)
    
def Stop () :
    

    GPIO.output(in1 , GPIO.HIGH)
            
    GPIO.output(in2 , GPIO.HIGH)
            
    GPIO.output(in3 , GPIO.HIGH)
            
    GPIO.output(in4 , GPIO.HIGH)
    