import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes

while True:
    try:
        X, y = load_diabetes(return_X_y=True)
        random_row = np.random.randint(0, X.shape[0] - 1)
        
        # Создание ID
        message_id = datetime.timestamp(datetime.now())
        
        # Подключение к RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        
        # Декларация очередей
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')
        
        # Формирование сообщений
        message_y_true = {'id': message_id, 'body': y[random_row]}
        message_features = {'id': message_id, 'body': list(X[random_row])}
        
        # Публикация сообщений
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        
        print(f"Отправлено: ID={message_id}, y_true={message_y_true['body']}, features={message_features['body']}")
        
        connection.close()
        time.sleep(5)  # Задержка 5 секунд
    except Exception as e:
        print(f"Ошибка: {e}")
