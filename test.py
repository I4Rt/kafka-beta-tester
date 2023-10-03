# from __future__ import annotations

# class test():
#     instance:test = None
#     val = None
#     def __init__(self, val):
#         self.val = val
    
#     def setInstance(val):
    
        
#         instance = test(val)
#         return instance
    
    
# a = test.setInstance(2)
# print(a.val)

from kafka import KafkaProducer, KafkaAdminClient  # pip3 install kafka-python

# k = KafkaProducer(bootstrap_servers="localhost:9092")
# print(k.config['api_version'])

# admin_client = KafkaAdminClient(bootstrap_servers=["localhost:9092"])
import cv2
from FileUtil import *
with open('output.txt', 'w') as file:
    img = cv2.imread('BigImage.jpg')
    
    imgB = FileUtil.convertImageToBytes(img, '.jpg')
    
    data = {"taskID": 14, "data": [{"img": imgB, "sectors": [{"points": [[68, 80.39999389648438], [41, 148.39999389648438], [100, 220.39999389648438], [250, 219.39999389648438], [281, 104.39999389648438], [278, 30.399993896484375], [74, 75.39999389648438]], "mode": 1}]}]}
    
    file.write(json.dumps(data))