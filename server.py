"""
Note:
    This is file is for the host machine which gets the images from the client using imagezmq server
    This file doesn't send images but recieves them from the client and recognize faces according to the dataset provided
"""

"""importing all the important files"""
import cv2
"""Imagezmq is a zmq library to send and recieve images over network"""
from Assets import imagezmq
import numpy as np 
import socket
"""vgg_model is out moduel to detect faces and recognize them"""
import vgg_model
import pymongo
import datetime
print(datetime.datetime.now().strftime("%H"),":",datetime.datetime.now().strftime("%M"),":",datetime.datetime.now().strftime("%S"))

"""initializing the server using imagezmq"""
#server_init = imagezmq.ImageHub(open_port='tcp://*:8008')
#hostname = socket.gethostname()
#ipaddress = socket.gethostbyname(hostname)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Ajna"]
coll = db["Person"]
"""Below code will show the ipaddress of the server it is using
Use this ip address in the client code to connect to this server"""
#print("Ip address of server: "+str(ipaddress))

blank = vgg_model.VggFaceNet()
detect = vgg_model.Detection()

#cam1 = cv2.VideoCapture("http://192.168.0.6:8081")
#cam2 = cv2.VideoCapture("http://192.168.0.6:8082")
vc = cv2.VideoCapture(0)
frame_count = 0

"""infinite loop to recieve image from client and show it on screen
    This loop can be broken by pressing the 'q' button"""
while True:
    frame_count = frame_count + 1
    """We recieve image and message from the client connected"""
#    (msg, frame) = server_init.recv_image()
#    ret1, frame1 = cam1.read()
#    ret2, frame2 = cam2.read()
    ret, frame = vc.read()

    """Time setting for entry of time stamp in database"""    
    date = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    year = datetime.datetime.now().strftime("%Y")
    hr = datetime.datetime.now().strftime("%H")
    mi = datetime.datetime.now().strftime("%M")
    sec = datetime.datetime.now().strftime("%S") 
    time = str(date)+"/"+str(month)+"/"+str(year)+"--"+str(hr)+":"+str(mi)+":"+str(sec)
    
    if frame_count%20 == 0:
        print("recognize==========================================================")
        faces = detect.detectFace(frame)
#        faces1 = detect.detectFace(frame1)
#        faces2 = detect.detectFace(frame2)
    
        for (x, y, w, h) in faces:
            faceimg = frame[y:y+h, x:x+w]
            scores = blank.recognize_from_encodings(faceimg)
            print("camera1==============================================================")
            print(scores)
            name = max(scores, key = scores.get)
            coll = db[name]
            coll.insert_one({"Camera":"1", "Time": time})
            print(name)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 1)
        cv2.imshow("frame1", frame)
            
#        for (x, y, w, h) in faces2:
#            faceimg = frame2[y:y+h, x:x+w]
#            scores = blank.recognize_from_encodings(faceimg)
#            print("camera2==============================================================")
#            print(scores)
#            name = max(scores, key = scores.get)
#            coll = db[name]
#            coll.insert_one({"Camera":"2", "Time": time})
#            print(name)
#            cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 1)
#            cv2.imshow("frame2", frame2)
#        cv2.imshow("frame2", frame2)
    else:
        cv2.imshow("frame1", frame)
#        cv2.imshow("frame2", frame2)
    """When we stop here we send a reply stop to the client to stop it."""
    if cv2.waitKey(1) & 0xFF == ord("q"):
#        server_init.send_reply(b'stop')
        break
    """Send reply to server to keep sending."""
#    server_init.send_reply(b'K')
#    cv2.imshow(msg, frame)
    
cv2.destroyAllWindows()        
vc.release()
#cam1.release()
#cam2.release()
    
"""This is test/debugging code """
#import vgg_model
#m = vgg_model.VggFaceNet()
#m.create_encodings()
#import pickle
#file = open("encodings.pk", "rb")
#encodings = pickle.load(file)
#for e in encodings:
#    print(e)
#    print(encodings[e])
#img = cv2.imread("1.jpg")
#img = cv2.resize(img, (500,600))
#faces = detect.detectFace(img)
#for (x,y,w,h) in faces:
#    cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 1)
#    faceimg = img[y:y+h, x:x+w]
#    scores = blank.recognize_from_encodings(faceimg)
#    print(scores)
#cv2.imshow("frame", img)    

#############################################
#vc = cv2.VideoCapture(0)
#while True:
#    ret, frame = vc.read()
#    faces = detect.detectFace(frame)
#    for (x,y,w,h) in faces:
#        faceimg = frame[y:y+h, x:x+w]
#        scores = blank.recognize_from_encodings(faceimg)
##        print(scores)
#        name = max(scores, key = scores.get)
#        print(name)
#        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 1)
#    
#    cv2.imshow("Frame", frame)
#    
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#vc.release()
#cv2.destroyAllWindows()



    
    
