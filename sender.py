from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import time
from threading import Condition
import conditionsHolder

def sendMessage(kafkaServer:str, topic:str, condId:int, n:int = 5, timeout = 1):
    time.sleep(2)
    counter = 0
    producer = KafkaProducer(bootstrap_servers=kafkaServer)
    for _ in range(n):
        counter += 1
        future = producer.send(topic, bytes(f'Message #{counter}', 'utf-8'))
        future.get()
        time.sleep(timeout)
    with conditionsHolder.conditions[condId]:
        if conditionsHolder.conditions[condId].wait():
            print('ready to send')
        else:
            print('Runtime')
        
        
def createTopic(kafkaServer, topicName):
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafkaServer, 
        client_id='test'
    )
    topic_list = []
    topic_list.append(NewTopic(name=topicName, num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    
        