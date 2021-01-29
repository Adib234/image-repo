from datetime import datetime
from pymongo import MongoClient
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from imageai.Classification import ImageClassification
import os
from flask import Flask, request, make_response, current_app, g
from flask_cors import CORS
import logging
import base64
from flask_api import status
import pprint
from elasticsearch import Elasticsearch

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

        app.logger.info("%s", data["tags"] in data)

        image_description = data["tags"]
        app.logger.info('%s is the image', image)
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

            return response
        else:
            response = {'file_name': image_name, 'tags': image_description}
            res = es.index(index="shopify-index", body=response)

            app.logger.info('%s is the elasticsearch response', res['result'])

            return response

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
            return status.HTTP_400_BAD_REQUEST  # existing user

        else:
            user["email"] = email
            password_hash = pwd_context.encrypt(password)
            user["password_hash"] = password_hash
            user["signed_up"] = datetime.utcnow()
            users.insert_one(user).inserted_id
            # app.logger.info('%s is the response', response)

            return {"data": 1}

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


# @app.route('/login', methods=['POST', 'OPTIONS'])
# def login():
#     if request.method == 'POST':
#         app.logger.info('%s is the request', request.json)

#         data = request.json
#         app.logger.info('%s is the data', data)

#         image = data["image"]
#         image_name = data["fileName"]

#         response = {'file_name': image_name, 'tags': final}

#         app.logger.info('%s is the response', response)

#         return response

#     elif request.method == "OPTIONS":  # CORS preflight
#         return _build_cors_prelight_response()
#     else:
#         raise RuntimeError(
#             "Weird - don't know how to handle method {}".format(request.method))


# @app.route('/logout', methods=['POST', 'OPTIONS'])
# def logout():
#     if request.method == 'POST':
#         app.logger.info('%s is the request', request.json)

#         data = request.json
#         app.logger.info('%s is the data', data)

#         image = data["image"]
#         image_name = data["fileName"]

#         response = {'file_name': image_name, 'tags': final}

#         app.logger.info('%s is the response', response)

#         return response

#     elif request.method == "OPTIONS":  # CORS preflight
#         return _build_cors_prelight_response()
#     else:
#         raise RuntimeError(
#             "Weird - don't know how to handle method {}".format(request.method))


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


# def verify_password(self, password):
#     return pwd_context.verify(password, self.password_hash)
