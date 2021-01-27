from imageai.Classification import ImageClassification
import os
from flask import Flask, request, make_response, current_app, g
from flask_cors import CORS
import logging
import base64
import sqlite3
import click
from flask.cli import with_appcontext
from models import User
from flask_api import status
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/tags', methods=['GET', 'POST', 'OPTIONS'])
def put_tags():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        image = data["image"]
        image_name = data["fileName"]
        # app.logger.info('%s is the image', image)

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

        response = {'file_name': image_name, 'tags': final}

        app.logger.info('%s is the response', response)

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

        if User.query.filter_by(email=email).first() is not None:
            return status.HTTP_400_BAD_REQUEST  # existing user

        else:

            user = User(email=email, password=password)
            user.hash_password(password)
            db.session.add(email)
            db.session.commit()
            #app.logger.info('%s is the response', response)

            return {"data": 1}

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

        image = data["image"]
        image_name = data["fileName"]

        response = {'file_name': image_name, 'tags': final}

        app.logger.info('%s is the response', response)

        return response

    elif request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        image = data["image"]
        image_name = data["fileName"]
        # app.logger.info('%s is the image', image)

        response = {'file_name': image_name, 'tags': final}

        app.logger.info('%s is the response', response)

        return response

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
