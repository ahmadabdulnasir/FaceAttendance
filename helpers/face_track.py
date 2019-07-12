import requests
import cv2

def regFace(imgs, userid, base_url='http://134.209.226.48:8088'):
    ''' registering unknown person to the db, takes in list of images files and a userid'''
    try:
        binimgs = [open(img, "rb").read() for img in imgs]
        go = 1
    except ValueError:
        print("[ERROR]: Please pass in imgs files names, not bytes like\n Trying filelike objects")
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
        
#OSError: [Errno 101] Network is unreachable

def preditFace(img, base_url='http://134.209.226.48:8088'):

    url = "{}/v1/vision/face/recognize".format(base_url)
    image_data = open(img,"rb").read()
    try:
        response = requests.post(url, files={"image":image_data}).json()
    except ConnectionError:
        print('No Connection')
    print(response)
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
        msg = "No face in image"
        print(msg)
        return None

if __name__ == "__main__":
    import numpy as np
    img = np.zeros( (100,100,3) )
    preditFace(img)
