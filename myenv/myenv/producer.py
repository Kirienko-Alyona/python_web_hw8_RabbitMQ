import random

from pymongo import MongoClient
import pika
from faker import Faker

from models import User
from connect import conn


fake = Faker()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='mail_service', exchange_type='direct')
    channel.exchange_declare(exchange='sms_service', exchange_type='direct')
    channel.queue_declare(queue='marketing_campaign_email', durable=True)
    channel.queue_declare(queue='marketing_campaign_sms', durable=True)
    channel.queue_bind(exchange='mail_service', queue='marketing_campaign_email')
    channel.queue_bind(exchange='sms_service', queue='marketing_campaign_sms')

    for count in range(1, 21):
        user = User(
            fullname=fake.name(),
            email=fake.ascii_free_email(),
            phone=fake.phone_number(),
            age=random.randint(21, 75),
           send_method=random.choice(["phone", "email"])
        ).save()

        channel.basic_publish(
            exchange='mail_service',
            routing_key='marketing_campaign_email',
            body=str(user.id).encode(), 
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
            
        channel.basic_publish(
            exchange='sms_service',
            routing_key='marketing_campaign_sms',
            body=str(user.id).encode(), 
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    connection.close()


if __name__ == '__main__':

    client = MongoClient(conn)
    db = client.mongo_db
    main()
    client.close()
