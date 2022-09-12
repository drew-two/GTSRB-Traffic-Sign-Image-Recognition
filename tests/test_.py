import base64
from pathlib import Path

from PIL import Image

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()

def read_image(file):
    test_directory = Path(__file__).parent

    return Image.open(test_directory / file)

def test_base64_decode_image():
    base64_input = read_text('image.b64')

    actual_result = model.base64_decode_image(base64_input)
    expected_result = read_image('0.png')

    assert actual_result == expected_result

def test_base64_decode():
    base64_input = read_text('result.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = {
        "sign_prediction": "Speed limit (20km/h) sign.",
        "sign_id": 0,
    }

    assert actual_result == expected_result

class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_lambda_handler():
    model_mock = ModelMock([1])
    model_version = 'Test123'
    model_service = model.ModelService(model_mock, model_version)

    base64_input = read_text('request.b64')

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'sign-classifier',
                'version': None,
                'prediction': {
                    'sign_prediction': "Speed limit (20km/h) sign.", 
                    'sign_id': 256
                    },
            }
        ]
    }

    assert actual_predictions == expected_predictions
