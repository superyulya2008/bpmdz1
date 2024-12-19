import pika
import pandas as pd
import json
import os

log_file = "./logs/metric_log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("id,y_true,y_pred,absolute_error\n")

# Буфер для хранения данных
data_buffer = {"y_true": {}, "y_pred": {}}

def callback_y_true(ch, method, properties, body):
    message = json.loads(body)
    data_buffer["y_true"][message["id"]] = message["body"]
    check_and_log(message["id"])

def callback_y_pred(ch, method, properties, body):
    message = json.loads(body)
    data_buffer["y_pred"][message["id"]] = message["body"]
    check_and_log(message["id"])

def check_and_log(message_id):
    if message_id in data_buffer["y_true"] and message_id in data_buffer["y_pred"]:
        y_true = data_buffer["y_true"].pop(message_id)
        y_pred = data_buffer["y_pred"].pop(message_id)
        abs_error = abs(y_true - y_pred)
        
        with open(log_file, "a") as f:
            f.write(f"{message_id},{y_true},{y_pred},{abs_error}\n")
        
        print(f"Лог добавлен: ID={message_id}, y_true={y_true}, y_pred={y_pred}, abs_error={abs_error}")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)

print("Сервис metric запущен. Ожидание сообщений...")
channel.start_consuming()
