from threading import Condition
from kafka import KafkaConsumer
import conditionsHolder
def reciever(kafkaServer:str, topic:str, condId:int):
    with conditionsHolder.conditions[condId]:
        consumer = KafkaConsumer( bootstrap_servers=[kafkaServer])
        consumer.subscribe(topic)
        if consumer.bootstrap_connected():
            conditionsHolder.conditions[condId].notify_all()
            print(f'on air: {topic}')
            for msg in consumer:
                print("Topic Name=%s,Message=%s"%(msg.topic,msg.value))
        
if __name__ == "__main__":

    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer( bootstrap_servers=['localhost:9092'])
    consumer.subscribe('test3_topic')
    print(consumer.bootstrap_connected())
    for msg in consumer:
        print("Topic Name=%s,Message=%s"%(msg.topic,msg.value))
    

