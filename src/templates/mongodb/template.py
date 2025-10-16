"""
Template para crear un servicio de MongoDB.
"""

class MongodbTemplate:

    @staticmethod
    def get_service_content():
        return """
import config.mongodb_config as connection
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

    @staticmethod
    def get_pipeline_publications_data_content():
        return """
def extract_publications_data():
    return [
        {
            "$unwind": {
                "path": "$variations"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "code": { "$first": "$code" },
                "country": { "$first": "$countryCode" },
                "title": { "$first": "$title" },
                "categoryCode": { "$first": "$product.categoryCode" },
                "brand": { "$first": "$product.brand.name" },
                "model": { "$first": "$product.model" },
                "year": { "$first": "$product.year" },
                "displacement": { "$first": "$product.displacement" },
                "type": { "$first": "$product.type" },
                "price_base": { "$first": "$price.base" },
                "price_currency": { "$first": "$price.currencyCode" },
                "price_net": { "$first": "$price.net" },
                "stock": { "$push": { "$toString": "$variations.stock" } },
                "total_weight": {
                    "$first": {
                        "$let": {
                            "vars": {
                                "tw": {
                                    "$filter": {
                                        "input": "$product.technicalSpecs",
                                        "as": "spec",
                                        "cond": { "$eq": ["$$spec.key", "total_weight"] }
                                    }
                                }
                            },
                            "in": {
                                "$ifNull": [
                                    {
                                        "$cond": [
                                            { "$gt": [ { "$size": "$$tw" }, 0 ] },
                                            { "$arrayElemAt": [ "$$tw.value", 0 ] },
                                            None
                                        ]
                                    },
                                    None
                                ]
                            }
                        }
                    }
                },
                "product_pictures": { "$first": "$product.pictures" },
                "published": { "$first": "$published" },
                "forwarding_code": { "$first": "$_forwardingCode" },
                "relevance": { "$first": "$relevance" },
                "tags": { "$push": "$filterTags" },
                "condition": { "$first": "$product.condition" }
            }
        },
        {
            "$project": {
                "_id": 1,
                "code": 1,
                "country": 1,
                "categoryCode": 1,
                "brand": 1,
                "model": 1,
                "year": 1,
                "displacement": 1,
                "type": 1,
                "price_base": 1,
                "price_currency": 1,
                "price_net": 1,
                "stock": 1,
                "published": 1,
                "forwarding_code": 1,
                "relevance": 1,
                "condition": 1,
                "total_weight": 1,
                "tags": 1,
                "product_pictures": { "$arrayElemAt": ["$product_pictures", 0] }
            }
        }
    ]

            """

    @staticmethod
    def get_pipeline_variations_data_content():
        return """
def extract_variation_data(countryCode: str, vehicle_type: str):
    '''
    Devuelve un pipeline de agregación para:
      - Unwind de variations
      - SKUs únicos
      - Lista completa de variaciones (sku, color, stock, status, precios)
      - Tags aplanados y deduplicados
    Si se pasa `code`, filtra por ese code específico (útil para debug).
    '''
    match_stage = {
        'countryCode': countryCode,
        'published': True,
        'product.categoryCode': f'{countryCode}-{vehicle_type}',
        '_forwardingCode': None
    }
    pipeline = [
        {
            '$match': match_stage
        },
        {
            '$unwind': '$variations'
        },
        {
            '$group': {
                '_id': {
                    'countryCode': '$countryCode',
                    'categoryCode': '$product.categoryCode',
                    'code': '$code',
                    'brand': '$product.brand.name',
                    'model': '$product.model',
                    'year': '$variations.year',
                    'type': '$product.type'
                },

                # SKUs únicos
                'skus': { '$addToSet': '$variations.sku' },

                # Normaliza color a array para luego aplanar, si lo necesitas más adelante
                'colorsRaw': {
                    '$addToSet': {
                        '$cond': [
                            { '$isArray': '$variations.color' },
                            '$variations.color',
                            [ '$variations.color' ]
                        ]
                    }
                },

                # Lista de variaciones (detalle por SKU/color)
                'variations_list': {
                    '$push': {
                        'sku': '$variations.sku',
                        'color': '$variations.color',
                        'stock': '$variations.stock',
                        'status': '$variations.status',
                        'price_base': '$variations.price.base',
                        'price_net': '$variations.price.net'
                    }
                },

                "total_weight": {
                                    "$first": {
                                        "$let": {
                                            "vars": {
                                                "tw": {
                                                    "$filter": {
                                                        "input": "$product.technicalSpecs",
                                                        "as": "spec",
                                                        "cond": { "$eq": ["$$spec.key", "total_weight"] }
                                                    }
                                                }
                                            },
                                            "in": {
                                                "$ifNull": [
                                                    {
                                                        "$cond": [
                                                            { "$gt": [ { "$size": "$$tw" }, 0 ] },
                                                            { "$arrayElemAt": [ "$$tw.value", 0 ] },
                                                            None
                                                        ]
                                                    },
                                                    None
                                                ]
                                            }
                                        }
                                    }
                                },

                # Campos constantes dentro del grupo
                'relevance': { '$first': '$relevance' },
                'condition': { '$first': '$product.condition' },

                # Recolecta tags (pueden venir como array)
                'tagsRaw': { '$push': '$filterTags' }
            }
        },
        {
            '$project': {
                '_id': 0,
                'countryCode': '$_id.countryCode',
                'categoryCode': '$_id.categoryCode',
                'code': '$_id.code',
                'brand': '$_id.brand',
                'model': '$_id.model',
                'year': '$_id.year',
                'type': '$_id.type',

                # Lista completa de variaciones
                'variations': '$variations_list',

                "total_weight": 1,

                'relevance': 1,
                'condition': 1,

                # Aplana y deduplica tags (evita array de arrays)
                'tags': {
                    '$setUnion': [
                        {
                            '$reduce': {
                                'input': '$tagsRaw',
                                'initialValue': [],
                                'in': { '$concatArrays': [ '$$value', '$$this' ] }
                            }
                        }
                    ]
                }
            }
        }
    ]

    return pipeline

        """


    # @staticmethod
    # def get_pipeline_publications_data_content():
    #     pass

    # @staticmethod
    # def get_pipeline_info_titles_data_content():
    #     pass