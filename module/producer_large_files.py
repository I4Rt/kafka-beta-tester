from kafka import KafkaProducer
from faker import Faker
import json
import time
import cv2
import base64


class KafkaProducerPlus:
    producer = None
    topic = None
    server = None

    def __init__(self, bootstrap_servers, topic, value_serializer):
        self.topic = topic
        self.server = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      value_serializer=value_serializer, max_request_size=10485880)

    def sendMessage(self, message):
        self.producer.send(self.topic, message)


    # def sendImage(self, image):
    #     _, encriptedImg = cv2.imencode(".jpg", image)
    #     imgAsStr = encriptedImg.tobytes()
    #     imgByteStr = base64.b64encode(imgAsStr).decode("utf-8")
    #     self.producer.send(self.topic, {"image": imgByteStr})

    def sendImage(self, jsn):
        self.producer.send(self.topic, jsn)

    def getTopic(self):
        return self.topic

    def getServer(self):
        return self.server


# fake = Faker()


# def get_registered_user():
#     return {"name": fake.name(),
#             "address": fake.address(),
#             "year": fake.year()}


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducerPlus(["localhost:9092"], topic="SO11_local",
                             value_serializer=json_serializer)

img = cv2.imread("image.jpg")


if __name__ == "__main__":
    while True:
        # registered_user = get_registered_user()
        # print(registered_user)
        #producer.sendMessage(registered_user)
#        with open("senderData.json") as f:
        with open("output.txt") as f:
            json_file = json.load(f)

        print(json_file)
        producer.sendImage(json_file)
        time.sleep(4)
