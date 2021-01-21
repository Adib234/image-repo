from imageai.Classification import ImageClassification
import os
from flask import Flask, request
from flask_cors import CORS
import logging
app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello_world():
    return {"What's": "up"}


@app.route('/tags', methods=['GET', 'POST'])
def put_tags():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        image = data["image"]
        app.logger.info('%s is the image', image)

        execution_path = os.getcwd()

        prediction = ImageClassification()
        # prediction.setModelTypeAsResNet50()
        # prediction.setModelTypeAsInceptionV3()
        prediction.setModelTypeAsDenseNet121()

        prediction.setModelPath(os.path.join(
            execution_path, "DenseNet-BC-121-32.h5"))
        prediction.loadModel()

        predictions, probabilities = prediction.classifyImage(
            os.path.join(execution_path, image), result_count=5)

        final = []
        for eachPrediction, eachProbability in zip(predictions, probabilities):
            final.append(eachPrediction)

        return {'tags': final}
