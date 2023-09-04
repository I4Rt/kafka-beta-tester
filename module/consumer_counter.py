from kafka import KafkaConsumer, KafkaProducer
import json
import cv2
import base64
from numpy import frombuffer

from flask import Flask, request, json
import warnings
from ultralytics import YOLO
from base64 import b64decode
from shapely.geometry import Point, Polygon
import os


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

    consumer  = KafkaConsumerPlus("SO1_receive",
                                  "localhost:9092",
                                  "earliest",
                                  "consumer-group-a")

    print("starting the consumer Counter")

    for msg in consumer.consumer:
        for key in json.loads(msg.value):
            if key == "counter":
               print(key, json.loads(msg.value)[key])
