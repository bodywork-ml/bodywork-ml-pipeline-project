"""
This module defines what will happen in stage-2-deploy-scoring-service.

curl http://0.0.0.0:5000/iris/v1/predict \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"X": [1, 2, 3, 4]}'
"""
from urllib.request import urlopen

import joblib
import numpy as np
from flask import Flask, jsonify, make_response, request, Response

app = Flask(__name__)


@app.route('/iris/v1/predict', methods=['GET', 'POST'])
def predict() -> Response:
    X = np.array([request.json['X']])
    predicted_class = (
        model
        .predict(X)
        .tolist()
        [0]
    )
    response_data = {
        'prediction': predicted_class,
        'model': str(model)
    }
    return make_response(jsonify(response_data))


if __name__ == '__main__':
    model_url = 'http://bodywork-example-ml-project.s3.eu-west-2.amazonaws.com/iris_tree_classifier.joblib'
    model = joblib.load(urlopen(model_url))
    app.run(host='0.0.0.0', port=5000)
