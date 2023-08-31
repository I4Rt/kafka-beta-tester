from kafka import KafkaConsumer
import json
import cv2
import base64
from numpy import frombuffer


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
    consumer  = KafkaConsumerPlus("registered_user1",
                                  "localhost:9092",
                                  "earliest",
                                  "consumer-group-a")
    print("starting the consumer")

    for msg in consumer.consumer:
        for key in json.loads(msg.value):
            if key == "image":
                readImgBytes = base64.b64decode(json.loads(msg.value)[key])
                npImg = frombuffer(readImgBytes, 'u1')
                decImg = cv2.imdecode(npImg, 1)
                cv2.imwrite("image_receive.jpg", decImg)
            print(key, json.loads(msg.value)[key])
#        print("Registered User = {}".format(json.loads(msg.value)))
