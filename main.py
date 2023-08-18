import threading
import asyncio 
import time

from config import *
from sender import *
from reciever import *

import conditionsHolder
def testFoo (a, b):
    counter = 1
    while True:
        yield f'Function ran {counter} times, param: {a, b}'
        counter += 1

def threadFoo(a, b, cond:Condition):
    with cond:
        if cond.wait():
            cnt = 0
            for i in testFoo(a, b):
                cnt += 1
                if cnt == 10:
                    break
                print(i)
                a += 1
                time.sleep(1)
        

# cond = threading.Condition()
# x = threading.Thread(target=threadFoo, args=(1, 'test', cond,))
# x.start()
# with cond:
#     time.sleep(5)
#     print('await is done')
#     cond.notify_all()
    

if __name__ == "__main__":
    conditionsHolder.conditions.append(threading.Condition())
    
    createTopic(kafkaServer=kafkaServer, topicName=topicName)
    r = threading.Thread(target=reciever, args=(kafkaServer, topicName, 0,))
    s = threading.Thread(target=sendMessage, args=(kafkaServer, topicName, 0, 5,))
    s.start()
    r.start()
    s.join()
    

        
        
    







'''



import threading, time

def consumer(cond, queue= None):
    """ждет определенного состояния для использования ресурсов"""
    th_name = threading.current_thread().name
    print(f'Запуск потока потребителя {th_name}')
    with cond:
        cond.wait()
        print(f'Обработка ресурса потребителем {th_name}')
        time.sleep(0.3)


def producer(cond, queue = None):
    """подготовка ресурса, для использования потребителями"""
    th_name = threading.current_thread().name
    print(f'Запуск потока производителя {th_name}')
    with cond:
        print(f'{th_name} готовит ресурс для потребителей')
        time.sleep(2)
        print(f'{th_name} ресурс ГОТОВ!')
        cond.notify_all()


# установка переменной условия
condition = threading.Condition()

# создание потоков потребителей
c1 = threading.Thread(name='Consumer-1', 
                      target=consumer,
                      args=(condition,))
c2 = threading.Thread(name='Consumer-2', 
                      target=consumer,
                      args=(condition,))
# создание потока потребителей производителя
p = threading.Thread(name='PRODUCER', 
                     target=producer,
                     args=(condition,))
c1.start()
c2.start()
p.start()




'''