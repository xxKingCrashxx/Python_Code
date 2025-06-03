import uuid
import os
from datetime import date, datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(".env")
DATABASE = os.getenv("MONGO_DATABASE")
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

MOWING_DB = MongoClient(CONNECTION_STRING)[DATABASE]
clients_collection = MOWING_DB.get_collection("clients")
mowing_log_collection = MOWING_DB.get_collection("mowing_log")

# Models
class Client:
    def __init__(self, client_name: str, client_id: str = None):
        self.client_name = client_name
        self.client_id = client_id or str(uuid.uuid4())
    
    def to_dict(self):
        return {
            'client_name': self.client_name,
            '_id': self.client_id
        }
    
    @classmethod
    def from_dict(cls, client_dict: dict):
        client_name = client_dict.get("client_name", None)
        client_id = client_dict.get("_id", None)

        return cls(
            client_name=client_name,
            client_id=client_id
        )

class MowingLog:
    def __init__(self, client_object: Client, amount_due, log_id=None, mowing_date=None, paid=False):
        self.log_id = log_id or str(uuid.uuid4())
        self.client = client_object
        self.amount_due = amount_due
        self.paid=paid
        self.mowing_date = datetime.strptime(mowing_date, "%Y-%m-%d").date() if mowing_date else date.today()

    def to_dict(self):
        return {
            '_id': self.log_id,
            'client': self.client.to_dict(),
            'mowing_date': str(self.mowing_date),
            'amount_due': self.amount_due,
            'paid': self.paid
        }
    
    @classmethod
    def from_dict(cls, mowing_log_dict: dict):
        log_id = mowing_log_dict.get("_id", None)
        client = mowing_log_dict.get("client", None)
        mowing_date = str(mowing_log_dict.get("mowing_date", None))
        amount_due = mowing_log_dict.get("amount_due", None)
        paid = mowing_log_dict.get("paid", False)

        return cls(
            client,
            amount_due,
            log_id, 
            mowing_date,
            paid
        )

# database functions
def client_exists(client_name):
    client = clients_collection.find_one({"client_name": client_name})
    return True if client else False

def create_client(client_name):
    new_client = Client(client_name)

    if not client_exists(client_name):
        result = clients_collection.insert_one({
            '_id': new_client.client_id,
            'client_name': new_client.client_name
        })
        return result.inserted_id
    return None

def create_mowing_log(client_name, amount_due, log_id=None, mowing_date=None, paid=False):
    fetched_client = get_client_by_name(client_name)
    mowing_log = MowingLog(fetched_client, amount_due, log_id, mowing_date, paid)

    result = mowing_log_collection.insert_one(mowing_log.to_dict())
    return result.inserted_id

def get_client_by_id(client_id):
    return Client.from_dict(clients_collection.find_one({'_id': client_id}))

def get_client_by_name(client_name): 
    return Client.from_dict(clients_collection.find_one({'client_name': client_name}))

def get_all_clients():
    return clients_collection.find({}).to_list()

def get_client_mowing_logs(client_name):
    return mowing_log_collection.find({"client.client_name": client_name}).to_list()

def get_mowing_log_by_id(mowing_log_id):
    return mowing_log_collection.find_one({"_id": mowing_log_id})