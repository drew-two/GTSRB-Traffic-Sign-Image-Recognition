import os
import json
import base64

import boto3
import mlflow
import numpy as np

from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

def get_model_location(model_name):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 'mlops-final-models')
    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '1')

    model_location = f"models:/{model_name}/Production"
    model_location = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model'

    return model_location


def load_model(model_name):
    model_path = get_model_location(model_name)
    model = mlflow.keras.load_model(
        model_uri=f"models:/{model_name}/Production",
        dst_path="../artifacts_local/",
    )
    return model

def base64_decode_image(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    return decoded_image

def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    sign_event = json.loads(decoded_data)
    return sign_event


class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def predict(self, img):
        prediction = self.model.predict(img)
        predicted_class = class_labels[np.argmax(prediction, axis=1)[0]]
        return predicted_class + " sign."

    def lambda_handler(self, event):
        # print(json.dumps(event))

        predictions_events = []

        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            sign_event = base64_decode(encoded_data)

            sign = sign_event['sign']
            sign_id = sign_event['sign_id']

            sign_image = base64_decode_image(sign)
            image_array = image.img_to_array(sign_image)
            image_batch = np.expand_dims(sign_image, axis=0)
            normalized = preprocess_input(image_batch)

            prediction = self.predict(normalized)

            prediction_event = {
                'model': 'sign_prediction_model',
                'version': self.model_version,
                'prediction': {'sign_prediction': prediction, 'sign_id': sign_id},
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

        return {'predictions': predictions_events}


class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        sign_id = prediction_event['prediction']['sign_id']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(sign_id),
        )


def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)


def init(prediction_stream_name: str, model_name: str, test_run: bool):
    model = load_model(model_name)

    callbacks = []

    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service
