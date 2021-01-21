from imageai.Classification import ImageClassification
import os

execution_path = os.getcwd()

prediction = ImageClassification()
# prediction.setModelTypeAsResNet50()
# prediction.setModelTypeAsInceptionV3()
prediction.setModelTypeAsDenseNet121()

prediction.setModelPath(os.path.join(
    execution_path, "DenseNet-BC-121-32.h5"))
prediction.loadModel()

predictions, probabilities = prediction.classifyImage(
    os.path.join(execution_path, "IMG_4466.JPG"), result_count=5)
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction, " : ", eachProbability)
