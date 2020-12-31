"""
This module defines what will happen in 'stage-1-train-model':

- download dataset;
- pre-process data into features and labels;
- train machine learning model; and,
- save model to cloud stirage (AWS S3).
"""
from datetime import datetime
from urllib.request import urlopen
from typing import Tuple

import boto3 as aws
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.base import BaseEstimator
from sklearn.metrics import f1_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

DATA_URL = ('http://bodywork-ml-pipeline-project.s3.eu-west-2.amazonaws.com'
            '/data/iris_classification_data.csv')
TRAINED_MODEL_AWS_BUCKET = 'bodywork-ml-pipeline-project'
TRAINED_MODEL_FILENAME = 'iris_tree_classifier.joblib'


def main() -> None:
    """Main script to be executed."""
    data = download_dataset(DATA_URL)
    features, labels = pre_process_data(data)
    trained_model = train_model(features, labels)
    persist_model(trained_model)


def download_dataset(url: str) -> pd.DataFrame:
    """Get data from cloud object storage."""
    print(f'downloading training data from {DATA_URL}')
    data_file = urlopen(url)
    return pd.read_csv(data_file)


def pre_process_data(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Prepare raw data for model training."""
    label_column = 'species'
    feature_columns = [
        'sepal length (cm)',
        'sepal width (cm)',
        'petal length (cm)',
        'petal width (cm)'
    ]
    classes_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
    X = data[feature_columns].values
    y = data[label_column].apply(lambda e: classes_map[e]).values
    return X, y


def log_model_metrics_to_stdout(
    y_actual: np.ndarray,
    y_predicted: np.ndarray
) -> None:
    """Print model evaluation metrics to stdout."""
    time_now = datetime.now().isoformat(timespec='seconds')
    accuracy = balanced_accuracy_score(
        y_actual,
        y_predicted,
        adjusted=True
    )
    f1 = f1_score(
        y_actual,
        y_predicted,
        average='weighted'
    )
    print(f'iris model metrics @{time_now}')
    print(f' |-- accuracy = {accuracy:.3f}')
    print(f' |-- f1 = {f1:.3f}')


def train_model(features: np.ndarray, labels: np.ndarray) -> BaseEstimator:
    """Train ML model."""
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.1,
        stratify=labels,
        random_state=42
    )
    print('training iris decision tree classifier')
    iris_tree_classifier = DecisionTreeClassifier(
        class_weight='balanced',
        random_state=42
    )
    iris_tree_classifier.fit(X_train, y_train)
    test_data_predictions = iris_tree_classifier.predict(X_test)
    log_model_metrics_to_stdout(y_test, test_data_predictions)
    return iris_tree_classifier


def persist_model(model: BaseEstimator) -> None:
    """Put trained model into cloud object storage."""
    dump(model, TRAINED_MODEL_FILENAME)
    try:
        s3_client = aws.client('s3')
        s3_client.upload_file(
            TRAINED_MODEL_FILENAME,
            TRAINED_MODEL_AWS_BUCKET,
            f'models/{TRAINED_MODEL_FILENAME}'
        )
        print(f'model saved to s3://{TRAINED_MODEL_AWS_BUCKET}'
              f'/{TRAINED_MODEL_FILENAME}')
    except Exception:
        print('could not upload model to S3 - check AWS credentials')


if __name__ == '__main__':
    main()
