#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import requests
import cv2
from helpers import paths
import os
#import io

def regFace(img, userid, base_url='http://localhost:8088'):
    ''' registering unknown person to the db, takes in image and a userid'''
    binimg = open(img, "rb").read()
    try:
        binimg = img
        go = 1
    except:
        print("[ERROR]: Matsala ta faru")
        go = 0
    if go:
        url = "{}/v1/vision/face/register".format(base_url)
        response = requests.post(url, files={"image":binimg},data={"userid":userid}).json()
        status = response['success']
        try:
            msg = response['message']
        except:
            msg = response['error']
        print("[INFO]: Response: {} ".format(status) )
        print("[INFO]: Status : ", msg)
        return msg
    else:
        print("[ERROR]: Error not finished")
        return None
    print("*"*40+'Done'+"*"*40)

def regFaces(imgs, userid, base_url='http://localhost:8088'):
    ''' registering unknown person to the db, takes in list of images files and a userid'''

    try:
        binimgs = [open(img, "rb").read() for img in imgs]
        go = 1
    except ValueError:
        print("[ERROR]: Please pass in imgs files names, not bytes like\n Trying filelike objects")
#        go = 0
        try:
            binimgs = imgs
            go = 1
        except:
            print("[ERROR]: Matsala ta faru")
            go = 0
    if go:
        for binimg in binimgs:
            url = "{}/v1/vision/face/register".format(base_url)
            response = requests.post(url, files={"image":binimg},data={"userid":userid}).json()
            status = response['success']
            try:
                msg = response['message']
            except:
                msg = response['error']
            print("[INFO]: Response: {} ".format(status) )
            print("[INFO]: Status : ", msg)
        return msg
    else:
        print("[ERROR]: Error not finished")
        return None
    print("*"*40+'Done'+"*"*40)



def preditFace(img, base_url='http://localhost:8088'):
    # from PIL import Image
    url = "{}/v1/vision/face/recognize".format(base_url)
    # predictionTemp = 'predicttmp'
    image_data = open(img,"rb").read()
    # image = Image.open(img).convert("RGB")
    try:
        response = requests.post(url, files={"image":image_data}).json()
    except ConnectionError:
        print('No Connection')
    print(response)
    #for face in response["predictions"]:

    status = response['success']
    try:
        face =  response["predictions"][0]
        msg = face['confidence']
        userid = face["userid"]
        y_max = int(face["y_max"])
        y_min = int(face["y_min"])
        x_max = int(face["x_max"])
        x_min = int(face["x_min"])
        # cropped = image.crop((x_min,y_min,x_max,y_max))
        # cropped.save("{}.jpg".format(predictionTemp))
        print("[INFO]: Confidence : ", msg)
        print("[INFO]: Response: {} ".format(status) )
        dta = {'userid':userid, 'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max , 'confidence': msg}
        # print(response)
        return dta

    except:
        msg = "No face Found"
        #print(response)
        return None

def train():
    sample_dir = 'data_sample'
    imagePaths = list(paths.list_images(sample_dir))

    if len(imagePaths) > 0:
        # for p in imagePaths:
        for (i, imagePath) in enumerate(imagePaths):
            print("[INFO]: Processing image {}/{}".format(i + 1, len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]
            print("[INFO]: Registering {}".format(name) )
            regFace()
    else:
        print('[ERROR]: {} is either empty or does not contain any image file'.format( os.path.abspath(sample_dir) ))

def tempFunc():
    sample_dir = 'data_sample'
    os.chdir(sample_dir)
    all_dirs = os.listdir()
    dirs = [dir for dir in all_dirs if os.path.isdir(dir)]
    for dir in dirs:
        print(dir)
        name = str(dir)
        print('[Name]: ', name)
        imagePaths = list(paths.list_images(dir))
        print(imagePaths)
        regFaces(imagePaths, name)
def boot():
    #train()
    sample_dir = 'data_sample/salafi'
    imagePaths = list(paths.list_images(sample_dir))
    # print(type(imagePaths))
    regFaces(imagePaths, 'salafi')
if __name__ == "__main__":
    # boot()
    tempFunc()
