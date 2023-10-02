from kafka import KafkaConsumer, KafkaProducer
import json
import cv2
import base64
import datetime
from numpy import frombuffer

from flask import Flask, request, json
import warnings
from ultralytics import YOLO
from base64 import b64decode
from shapely.geometry import Point, Polygon
import os

from  producer import KafkaProducerPlus, json_serializer

model = YOLO('yolov8n.pt')
warnings.filterwarnings("ignore")
app = Flask(__name__)

producer = KafkaProducerPlus(["localhost:9092"], topic="SO1_receive",
                             value_serializer=json_serializer)

def checkIfInside(border, target):
    """Checking if point in polygon or not."""
    return Polygon(border).contains(Point(target[0], target[1]))

def recognition(image, sectors, taskID):
    """Recognition image and send the counter."""
    #image = cv2.imread("queue/image_receive.jpg")

    results = model.predict(source=image, imgsz=1920, conf=0.25, classes=[0])
    decImg_h, decImg_w = image.shape[:2]

    #coords = {"coordinates": [[3.6, 50.4], [6.1, 95.1], [85.2, 96.1], [85.0, 96.1], [90.2, 86.3], [89.3, 37.2]]}
    counter = 0
    for sector in sectors:
        # if sector["mode"] == 1
        border = []
        print("len", len(sector["points"]))
        if len(sector["points"]) != 0:
            for coord in sector["points"]:
                border.append((round(coord[0] * decImg_w / 100), round(coord[1] * decImg_h / 100)))
            border.append(border[0])
        else:
            border.append([0, 0])
            border.append([decImg_w, 0])
            border.append([decImg_w, decImg_h])
            border.append([0, decImg_h])

        # Check our person in polygon it or not
        boxes = results[0].boxes
        for box in boxes:
            if checkIfInside(border, (box.xyxy[0][0].item(), box.xyxy[0][3].item())) and \
                    checkIfInside(border, (box.xyxy[0][2].item(), box.xyxy[0][3].item())):
                counter += 1

    producer.sendMessage({"taskID":  taskID, "counter": counter, "datetime": str(datetime.datetime.now())})

    return


class KafkaConsumerPlus:
    consumer = None
    topic = None
    server = None
    group_id = None
    auto_offset_reset = None

    def __init__(self, topic, bootstrap_servers, auto_offset_reset, group_id):
        self.topic = topic
        self.server = bootstrap_servers
        self.auto_offset_reset = auto_offset_reset
        self.group_id = group_id
        self.consumer = KafkaConsumer(self.topic,
                                      bootstrap_servers=self.server,
                                      auto_offset_reset=self.auto_offset_reset,
                                      group_id=self.group_id)

    def getTopic(self):
        return self.topic

    def getGroup(self):
        return self.group


if __name__ == "__main__":
    if not os.path.isdir('queue'):
        os.mkdir('queue')

    consumer  = KafkaConsumerPlus("SO1_local",
                                  "localhost:9092",
                                  "earliest",
                                  "consumer-group-a")

    print("starting the consumer ImageReceiver")

    for msg in consumer.consumer:
        for key_main in json.loads(msg.value):
            print("key_main", key_main)
            if key_main == "data":
                print('data')
                for key_data in json.loads(msg.value)["data"]:
                    readImgBytes = base64.b64decode(key_data["img"])
                    npImg = frombuffer(readImgBytes, 'u1')
                    decImg = cv2.imdecode(npImg, 1)
                    cv2.imwrite("queue/image_receive.jpg", decImg)
                    recognition(decImg, key_data["sectors"], json.loads(msg.value)["taskID"])
                    print("Sending")
#        print("Registered User = {}".format(json.loads(msg.value)))
