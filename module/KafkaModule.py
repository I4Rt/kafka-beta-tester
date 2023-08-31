from __future__ import annotations
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import time
import config


class KafkaBasics:
    _server = None
    _topic = None
    _topicIsChecked = False

    def __init__(self, topic, server):
        self._server = server
        self._topic = topic

    def _createTopic(self):
        admin_client = KafkaAdminClient(
            bootstrap_servers=self._server, 
            client_id=str(time.time())
        )
        topic_list = []
        topic_list.append(NewTopic(name=self._topic, num_partitions=1, replication_factor=1))
        try:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except:
            pass
        self._topicIsChecked = True

    def getTopic(self):
        return self._topic

    def getServer(self):
        return self._server


class KafkaSender(KafkaBasics):
    __instance: KafkaSender = None
    __producer: KafkaProducer | None = None

    def __init__(self, topic, server):
        KafkaBasics.__init__(self, topic, server)
        self.__producer = KafkaProducer(bootstrap_servers=self._server)

    @classmethod
    def setInstance(cls, topic:str, server:str = "localhost:9092") -> KafkaSender:
        if cls.__instance is not None:
            if cls.__instance.__producer is not None:
                cls.__instance.__producer.close()
                cls.__instance.__producer = None
        cls.__instance = KafkaSender(topic, server)
        return cls.__instance

    @classmethod
    def getInstance(cls) -> KafkaSender | None:
        return cls.__instance

    '''
    returns:
        # 0 - no instance
        # 1 - topic creation error
        # 2 - not initializated producer
        # 3 - time is out
        # data - ok
    '''
    def sendMessage(self, message):
        try:
            if not self._topicIsChecked:
                self._createTopic()
        except:
            return 1
        if self.__producer is not None:
            try:
                future = self.__producer.send(self._topic, bytes(message, 'utf-8'))
                data = future.get() 
                print(data)
                return data
            except:
                return 3
        else:
            return 2


class KafkaReceiver(KafkaBasics):
    __instance: KafkaReceiver = None
    __consumer: KafkaConsumer | None = None

    def __init__(self, topic, server, group_id):
        KafkaBasics.__init__(self, topic, server)
        cns = KafkaConsumer(topic, bootstrap_servers=self._server, group_id=group_id)
        try:
            if not self._topicIsChecked:
                self._createTopic()
        except:
            raise Exception('Topic create error')
        cns.subscribe(self._topic)
        self.__consumer = cns
        
    @classmethod
    def setInstance(cls, topic: str, server: str = "localhost:9092", group_id=None) -> KafkaReceiver:
        if cls.__instance is not None:
            if cls.__instance.__consumer is not None:
                cls.__instance.__consumer.close()
                cls.__instance.__consumer = None
        cls.__instance = KafkaReceiver(topic, server, group_id)
        return cls.__instance

    @classmethod
    def getInstance(cls) -> KafkaReceiver | None:
        return cls.__instance

    def receive(self):
        if self.__consumer is not None:
            try:
                
                for msg in self.__consumer:
                    yield msg
            except:
                raise Exception('Message recieving error')
        else:
            raise Exception('No consumer')


class KafkaGroup():
    items = []

    def __init__(self):
        self.items = []

    def append(self, item: KafkaReceiver):
        self.items.append(item)


if __name__ == "__main__":
    import threading

    def printer(receiver: KafkaReceiver):
        for msg in receiver.receive():
            print("Topic Name=%s,Message=%s"%(msg.topic,msg.value))

    topic = 'module_topic3'
    group_id = 'test_group'
    receiver = KafkaReceiver.setInstance(topic, config.kafkaServer, group_id)
    t = threading.Thread(target=printer, args=(receiver, ))
    t.start()
    time.sleep(5)
    sender = KafkaSender.setInstance(topic, config.kafkaServer)
    sender.sendMessage('test_message1')
    time.sleep(5)
    sender.sendMessage('test_message2')
    t.join()
