"""
This module defines what will happen in stage-1-train-model.
"""
from datetime import datetime
from urllib.request import urlopen

import boto3
import pandas as pd
from joblib import dump
from sklearn.metrics import f1_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data_url = 'http://bodywork-example-ml-project.s3.eu-west-2.amazonaws.com/iris_classification_data.csv'
data = pd.read_csv(urlopen(data_url))


def log_metrics_summary(y_actual, y_predicted):
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
    print(f'@{time_now}')
    print(f'-- accuracy = {accuracy:.3f}')
    print(f'-- f1 = {f1:.3f}')


def train():
    feature_columns = [
        'sepal length (cm)',
        'sepal width (cm)',
        'petal length (cm)',
        'petal width (cm)'
    ]

    label_column = 'species'
    classes_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}

    X = data[feature_columns].values
    y = data[label_column].apply(lambda e: classes_map[e]).values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.1,
        stratify=y,
        random_state=42
    )

    iris_tree_classifier = DecisionTreeClassifier(
        class_weight='balanced',
        random_state=42
    )
    iris_tree_classifier.fit(X_train, y_train)

    log_metrics_summary(y_test, iris_tree_classifier.predict(X_test))

    model_filename = 'iris_tree_classifier.joblib'
    dump(iris_tree_classifier, model_filename)

    s3_bucket_name = 'bodywork-example-ml-project'
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(
            model_filename,
            s3_bucket_name,
            model_filename
        )
    except Exception:
        print('could not upload model to S3')


if __name__ == '__main__':
    train()
