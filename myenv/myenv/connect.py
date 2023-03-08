from mongoengine import connect
import configparser


config = configparser.RawConfigParser()
res = config.read('./myenv/myenv/config.ini')
mongo_user = config.get('DB', 'user')
mongodb_password = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# connect to cluster on AtlasDB with connection string
conn = f"""mongodb+srv://{mongo_user}:{mongodb_password}@{domain}/{db_name}?retryWrites=true&w=majority"""
connect(host=conn, ssl=True)
