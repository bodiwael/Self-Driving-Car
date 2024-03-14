# load config
import json
import serial

from Lane_Algorithm import getlanecurve

with open('roboflow_config.json') as f:
    config = json.load(f)

    ROBOFLOW_API_KEY = config["ROBOFLOW_API_KEY"]
    ROBOFLOW_MODEL = config["ROBOFLOW_MODEL"]
    ROBOFLOW_SIZE = config["ROBOFLOW_SIZE"]

    FRAMERATE = config["FRAMERATE"]
    BUFFER = config["BUFFER"]


import asyncio
import cv2
import base64
import numpy as np
import httpx
import time
import Action
 

arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
# Construct the Roboflow Infer URL
# (if running locally replace https://detect.roboflow.com/ with eg http://127.0.0.1:9001/)
upload_url = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?api_key=",
    ROBOFLOW_API_KEY,
    #"&format=image", # Change to json if you want the prediction boxes, not the visualization
    "&format=json"
    "&stroke=5",
    "&labels=on"
])

# Get webcam interface via opencv-python
video = cv2.VideoCapture(0)

# Infer via the Roboflow Infer API and return the result
# Takes an httpx.AsyncClient as a parameter
async def infer(requests):
    # Get the current image from the webcam
    intialTrackBarVals = [ 101 , 0 , 0 , 100 ]
    
    Action.initializeTrackbars(intialTrackBarVals)
    
    curveList = []
    
    ret, img = video.read()
    
    curve = getlanecurve(img , display = 1)
        
    print(curve)
    
    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, channels = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)
 
    # Get prediction from Roboflow Infer API
    resp = await requests.post(upload_url, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    json_string = resp.content.decode('utf-8')
    json_dict = json.loads(json_string)
    predictions = json_dict['predictions']
    classes = [p['class'] for p in predictions]

    print(classes)
    # Parse result image
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    
    if(classes == 'stop sign'):
         
         value = write_read(str(1))
         time.sleep(0.5)
         print(value) # printing the value
   
    elif(classes == '120 speed limit'):
         value = write_read(str(2))
         time.sleep(0.5)
         print(value) 
         
    elif(classes == 'speed bump'):
         value = write_read(str(3))
         time.sleep(0.5)
         print(value) 
         
    elif(classes == '60 speed limit'):
         value = write_read(str(4))
         time.sleep(0.5)
         print(value) 
         
    elif(classes == '90 speed limit'):
         value = write_read(str(5))
         time.sleep(0.5)
         print(value) 
         
    if curve > 0.65 :
        
#             Carmove.Left()
#         print("Left !!")
         value = write_read(str(6))
         time.sleep(0.5)
         print(value) 
    
    elif curve < -0.65 :
        
#         print("Right !!")
         value = write_read(str(7))
         time.sleep(0.5)
         print(value)           
        
    else :
        
#          print("Forward !!!")
         value = write_read(str(8))
         time.sleep(0.5)
         print(value) 
    #image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return classes
    return image

# Main loop; infers at FRAMERATE frames per second until you press "q"
async def main():
    # Initialize
    last_frame = time.time()

    # Initialize a buffer of images
    futures = []

    async with httpx.AsyncClient() as requests:
        while 1:
            # On "q" keypress, exit
            if(cv2.waitKey(1) == ord('q')):
                break

            # Throttle to FRAMERATE fps and print actual frames per second achieved
            elapsed = time.time() - last_frame
            await asyncio.sleep(max(0, 1/FRAMERATE - elapsed))
            #print((1/(time.time()-last_frame)), " fps")
            last_frame = time.time()

            # Enqueue the inference request and safe it to our buffer
            task = asyncio.create_task(infer(requests))
            futures.append(task)

            # Wait until our buffer is big enough before we start displaying results
            if len(futures) < BUFFER * FRAMERATE:
                continue

            # Remove the first image from our buffer
            # wait for it to finish loading (if necessary)
            image = await futures.pop(0)
            # And display the inference results
          #  cv2.imshow('image', image)

# Run our main loop
asyncio.run(main())

# Release resources when finished
video.release()
cv2.destroyAllWindows()
