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

k = KafkaProducer(bootstrap_servers="localhost:9092")
print(k.config['api_version'])

admin_client = KafkaAdminClient(bootstrap_servers=["localhost:9092"])
