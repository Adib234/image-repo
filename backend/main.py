from datetime import datetime, timedelta
from pymongo import MongoClient
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from imageai.Classification import ImageClassification
import os
from flask import Flask, request, make_response, current_app, jsonify
from flask_cors import CORS
import logging
import base64
from flask_api import status
import pprint
from elasticsearch import Elasticsearch
import redis
import sys

es = Elasticsearch()


app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)


connection = os.environ.get(
    'MONGO_URI', '/Users/admin/shopifysummer2021/backend')


client = MongoClient(connection)


user = {"email": "",  "password_hash": "", "images_private": [],
        "bucket_name": [], "signed_up": None}

db = client["shopify-mongo"]
users = db["users"]


@app.route('/tags', methods=['GET', 'POST', 'OPTIONS'])
def put_tags():

    if request.method == 'POST':

        data = request.json

        image = data["image"]
        image_name = data["fileName"]
        image_description = data["tags"]
        private = data["private"]
        email = data["email"]
        if private:
            users.update_one({"email": email}, {
                '$push': {'images_private': image_name}})

        if len(image_description) == 0:
            execution_path = os.getcwd()

            prediction = ImageClassification()

            prediction.setModelTypeAsDenseNet121()

            prediction.setModelPath(os.path.join(
                execution_path, "DenseNet-BC-121-32.h5"))
            prediction.loadModel()

            imgdata = base64.b64decode(image)

            filename = 'image.jpg'

            with open(filename, 'wb') as f:
                f.write(imgdata)

            predictions, probabilities = prediction.classifyImage(
                os.path.join(execution_path, filename), result_count=5)

            os.remove(filename)

            final = []
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                final.append(eachPrediction)

            final_string = ' '.join(final)
            response = {'file_name': image_name,
                        'tags': final_string, 'timestamp': datetime.utcnow()}

            res = es.index(index="shopify-index", body=response)

            app.logger.info('%s is the elasticsearch response', res['result'])

            return add_success_headers(1)
        else:
            response = {'file_name': image_name, 'tags': image_description}
            res = es.index(index="shopify-index", body=response)

            app.logger.info('%s is the elasticsearch response', res['result'])
            return add_success_headers(1)

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/search', methods=['POST', 'OPTIONS'])
def search():
    if request.method == 'POST':

        data = request.json

        query = data["query"]
        permissions = data["permissions"]
        email = data["email"]
        if permissions == "Public":
            es.indices.refresh(index="shopify-index")

            res = es.search(index="shopify-index",
                            body={"query": {"match": {"tags": query}}})

            app.logger.info("Got %d Hits:" % res['hits']['total']['value'])

            res["hits"]["hits"] = res["hits"]["hits"][:5]
            app.logger.info(len(res['hits']['hits']))
            return add_success_headers(res["hits"]["hits"])

        elif permissions == "Private":
            es.indices.refresh(index="shopify-index")

            res = es.search(index="shopify-index",
                            body={"query": {"match": {"tags": query}}})

            app.logger.info("Got %d Hits:" % res['hits']['total']['value'])

            # res["hits"]["hits"]
            final = []

            for hit in res['hits']['hits']:
                if hit in users.find_one({"email": email})['bucket_name']:
                    final.append(hit)
            app.logger.info(len(final))
            return add_success_headers(final)

        else:
            return {"data": "", "status": 404, "statusText": 'OK', "headers": {}, "config": {}}

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        email = data["email"]
        password = data["password"]
        # users.insert_one(user).inserted_id

        if users.count_documents({"email": email}) >= 1:
            # existing user
            # test later if this works, we should be getting an error
            return {"data": "", "status": 404, "statusText": 'OK', "headers": {}, "config": {}}

        else:
            user["email"] = email
            password_hash = pbkdf2_sha256.hash(password)
            user["password_hash"] = password_hash
            user["signed_up"] = datetime.utcnow()
            users.insert_one(user).inserted_id
            # app.logger.info('%s is the response', response)

            return add_success_headers(1)

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        email = data["email"]
        password = data["password"]

        if users.count_documents({"email": email}) == 0:
            return {"data": "", "status": 404, "statusText": 'OK', "headers": {}, "config": {}}

        else:

            user_info = users.find_one({"email": email})
            app.logger.info("%s is the hashed password",
                            user_info["password_hash"])

            if pbkdf2_sha256.verify(password, user_info["password_hash"]):
                return add_success_headers(1)
            else:
                return {"data": "", "status": 404, "statusText": 'OK', "headers": {}, "config": {}}

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route("/add_bucket_name", methods=['POST', 'OPTIONS'])
def add_bucket_name():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        email = data["email"]
        bucket_name = data["bucketName"]

        app.logger.info('%s is the', users.find_one(
            {"email": email})['bucket_name'])
        if bucket_name in users.find_one({"email": email})['bucket_name']:
            return {"data": "", "status": 404, "statusText": 'OK', "headers": {}, "config": {}}
        else:
            users.update_one({"email": email}, {
                '$push': {'bucket_name': bucket_name}})

            return add_success_headers(1)

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route("/get_all_buckets", methods=['POST', 'OPTIONS'])
def get_all_buckets():
    if request.method == 'POST':

        data = request.json
        app.logger.info('%s is the data', data)

        response = cache_buckets(data["email"])
        app.logger.info('%s is the data', response)

        return add_success_headers(response[data['email']])

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def add_success_headers(data):
    response = make_response(jsonify(data))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('status', 200)
    response.headers.add('statusText', 'OK')
    return response


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()


def get_routes_from_cache(key: str) -> str:
    """Data from redis."""

    val = client.get(key)
    return val


def set_routes_to_cache(key: str, value: str) -> bool:
    """Data to redis."""

    state = client.setex(key, timedelta(seconds=3600), value=value,)
    return state


def cache_buckets(email: str) -> dict:

    # First it looks for the data in redis cache
    data = get_routes_from_cache(key=email)

    # If cache is found then serves the data from cache
    if data is not None:
        data = json.loads(data)
        data["cache"] = True
        return data

    else:
        # If cache is not found then sends request to database

        user_info = users.find_one({"email": email})

        data = {email: user_info["bucket_name"]}

        # This block sets saves the respose to redis and serves it directly
        if data.get("code") == "Ok":
            data["cache"] = False
            data = json.dumps(data)
            state = set_routes_to_cache(key=email, value=data)

            if state is True:
                return json.loads(data)
        return data
