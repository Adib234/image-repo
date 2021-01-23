from imageai.Classification import ImageClassification
import os
from flask import Flask, request
from flask_cors import CORS
import logging
import base64
app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/')
def hello_world():
    return {"What's": "up"}


@app.route('/tags', methods=['GET', 'POST', 'OPTIONS'])
def put_tags():
    if request.method == 'POST':
        app.logger.info('%s is the request', request.json)

        data = request.json
        app.logger.info('%s is the data', data)

        image = data["image"]
        app.logger.info('%s is the image', image)

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

        response = {'tags': final}

        app.logger.info('%s is the response', response)

        return response

    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))
