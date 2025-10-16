"""
Template para crear un servicio de MongoDB.
"""

class MongodbTemplate:

    @staticmethod
    def get_service_content():
        return """
import mongodb.mongodb_connection as connection
from mongodb.pipelines.extract_variation_data import extract_variation_data
from mongodb.pipelines.extract_publications_data import extract_publications_data
from mongodb.pipelines.extract_info_titles import extract_info_titles_data

class MongoDBFunctions:
    def __init__(self):
        self.client = connection.connect_mongodb()

    def list_collections(self):
        db = self.client.db_marketplace
        return db.list_collection_names()

    def select_collection(self, collection_name):
        db = self.client.db_marketplace
        collection = db[collection_name]
        return collection

    def variation_data_aggregation(self, collection_name, countryCode, vehicle_type):
        if countryCode not in ["MX", "CO", "CL", "PE"] or vehicle_type not in ["MOTORCYCLES", "CARS"]:
            print(f"Country code {countryCode} or vehicle type {vehicle_type} not supported")
            return None
        else:
            pipeline = extract_variation_data(countryCode, vehicle_type)
            collection = self.select_collection(collection_name)
            results = list(collection.aggregate(pipeline))

        return results

    def publications_data_aggregation(self, collection_name):
        pipeline = extract_publications_data()
        collection = self.select_collection(collection_name)
        results = list(collection.aggregate(pipeline))

        return results

    def publications_title_data_aggregation(self, collection_name, countryCode, vehicle_type):
        pipeline = extract_info_titles_data(countryCode, vehicle_type)
        collection = self.select_collection(collection_name)
        results = list(collection.aggregate(pipeline))

        return results
        """

    @staticmethod
    def get_config_content():
        return """
from pymongo import MongoClient
from dotenv import load_dotenv
import socks
import socket
import os
load_dotenv()

proxy_host = "localhost"
proxy_port = 9090

def connect_mongodb():
    socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
    socket.socket = socks.socksocket
    client = MongoClient(generate_url(os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD")))
    return client

def generate_url(username, password):
    return f"mongodb://{username}:{password}@shared-shard-00-00.eh6ne.mongodb.net:27017,shared-shard-00-01.eh6ne.mongodb.net:27017,shared-shard-00-02.eh6ne.mongodb.net:27017/?replicaSet=atlas-48izhi-shard-0&ssl=true&authSource=admin"
        """
