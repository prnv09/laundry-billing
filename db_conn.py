from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os 
import urllib.parse

#mongo_uri = os.getenv('MONGO_URI')

# password = "Pr09@mongodb"
# encoded_password = urllib.parse.quote_plus(password)
# print(encoded_password)
#encoded_username = urllib.parse.quote_plus("pranavkumbhar727")
# print(encoded_password)

#MONGO_URI = 'mongodb+srv://{encoded_username}:Prnv09mongo@cluster0.jd0soty.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
MONGO_URI = 'mongodb+srv://pranav:KxbEicxJ4HCbjKyN@cluster0.jd0soty.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
#MONGO_URI = 'mongodb://Vr%40kavkav:Vr%40kavkav@cluster0.w1o6reh.mongodb.net/'
#MONGO_URI = 'mongodb+srv://ashsih_kuldeep:eXhHmvTwXZMlhHSA@cluster0.w1o6reh.mongodb.net/Restaurant_AR'

#print(MONGO_URI)
#mongodb+srv://pranavkumbhar727:<password>@cluster0.jd0soty.mongodb.net/
def connect_to_mongodb():
    try:
        client = MongoClient(MONGO_URI,server_api=ServerApi('1'))
        print("connected to client")
        # database = client['you-laundry']
        # collection = database['orders']
        # cursor = collection.find()
        # for document in cursor:
        #     print(document)
        # print(cursor)
        client.admin.command('ping')
        print("Connected to MongoDB")
        db = client["you-laundry"]
        return client,db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

#connect_to_mongodb()
