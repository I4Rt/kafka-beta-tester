from __future__ import annotations
from typing import List
import cv2
from numpy import frombuffer
import json
import base64
import base128

class FileUtil:
    def __init__(self):
        pass
    
    @staticmethod
    def convertImageToBytes(img, imgType = '.png') -> str:
        _, encriptedImg = 	cv2.imencode(imgType, img)
        imgAsStr = encriptedImg.tostring()
        imgByteStr = base64.b64encode(imgAsStr).decode("utf-8")
        return imgByteStr
    
    @staticmethod
    def convertBytesToImg(encImg: str):
        readImgBytes = base64.b64decode(encImg)
        npImg = frombuffer(readImgBytes,'u1') 
        decImg = cv2.imdecode(npImg, 1)
        return decImg
    
    def convertImageToBytes85(img, imgType = '.png') -> str:
        _, encriptedImg = 	cv2.imencode(imgType, img)
        imgAsStr = encriptedImg.tostring()
        imgByteStr = base64.b85encode(imgAsStr).decode("utf-8")
        return imgByteStr
    
    

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    print(FileUtil.convertImageToBytes(img))
    
    
    