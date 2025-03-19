import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI", )

def get_db():
    client = MongoClient(
                        MONGO_URI,
                        tls=True,
                        tlsAllowInvalidCertificates=True,
                        serverSelectionTimeoutMS=5000,
                        )
    return client.get_database("task_manager")  # Database name
