import pika
import time
from pymongo import MongoClient

from models import User
from connect import conn


def send_sms(phone, str):
    pass


def callback(ch, method, properties, body):
    _id = body.decode()
    users = User.objects(id=_id, send_sms=False)
    for user in users:
        if user and user.send_method == 'phone':
            phone = user.phone
            fullname = user.fullname
            send_sms(phone, f"<h1> Hello <span>{fullname}</span></h1>")
            User.objects(id=_id).update_one(send_sms=True)
            time.sleep(1)
            print(f" [x] Done: {fullname}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='marketing_campaign_sms', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='marketing_campaign_sms', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':

    client = MongoClient(conn)
    db = client.mongo_db
    main()
    client.close()
