

kafkaServer = "localhost:9092"
with open('counter.txt', 'r') as file:
    counter = curCounter = int(file.read())
    curCounter += 1
with open('counter.txt', 'w') as file:
    file.write(str(curCounter))
topicName = f'test{counter}_topic'
groopId = 'test-groop'