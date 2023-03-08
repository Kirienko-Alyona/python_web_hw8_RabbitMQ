import pika
import time
from pymongo import MongoClient

from models import User
from connect import conn


def send_email(email, str):
    pass


def callback(ch, method, properties, body):
    _id = body.decode()
    users = User.objects(id=_id, send_email=False)
    for user in users:
        if user and user.send_method == 'email':
            email = user.email
            fullname = user.fullname
            send_email(email, f"<h1> Hello <span>{fullname}</span></h1>")
            User.objects(id=_id).update_one(send_email=True)
            time.sleep(1)
            print(f" [x] Done: {fullname}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='marketing_campaign_email', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='marketing_campaign_email', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':

    client = MongoClient(conn)
    db = client.mongo_db
    main()
    client.close()
