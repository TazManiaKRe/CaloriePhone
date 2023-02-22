#!/usr/bin/env python3

from flask import Flask, request, send_from_directory, jsonify
import numpy as np
import pandas as pd
import keras.utils
import sklearn.preprocessing
import sklearn.model_selection
import json
import tempfile
import f1

# constants
IMG_SHAPE = (299,299,3)
PREDICTION_CUTOFF = 0.25

# globals
app = Flask(__name__, static_folder="build/static")
model = None
translation = None
mlb = None

def predict(image_path):

    # read image as model input
    image = keras.utils.load_img(image_path, target_size=IMG_SHAPE)
    image = keras.utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # predict image labels
    prediction = (model.predict(image) > PREDICTION_CUTOFF).astype('int')
    prediction = pd.Series(prediction[0])
    prediction.index = mlb.classes_
    prediction = prediction[prediction==1].index.values

    # return predicted labels
    return list(prediction)

@app.route("/", methods=["GET"])
def r_main_page():
    return send_from_directory('build', 'index.html')

@app.route("/favicon.ico", methods=["GET"])
def r_favicon():
    return send_from_directory('.', 'favicon.ico')

@app.route("/prediction", methods=["POST"])
def r_prediction():

    predictions = []

    # create new temporary file for the image
    with tempfile.NamedTemporaryFile() as tmp:

        # write image to temp file
        tmp.write(request.get_data())

        # generate predictions
        predictions = predict(tmp.name)

    # make predictions a dictionary of predicted labels and their calories
    predictions = { prediction:translation[prediction] for prediction in predictions }

    # return predictions
    return jsonify(predictions)

if __name__ == "__main__":

    # load model
    model = keras.models.load_model("./caloriephone_model",  custom_objects={
        "macro_f1": f1.macro_f1,
        "macro_soft_f1": f1.macro_soft_f1
    })

    # read translation file
    with open("translation.json", 'r') as translation_file:
        translation = json.loads(translation_file.read())

    # init and configure multilabelbinarizer
    mlb = sklearn.preprocessing.MultiLabelBinarizer()
    mlb.fit([ [label] for label in list(translation.keys()) ])

    # run server
    app.run(host='0.0.0.0', port=8080)
    
