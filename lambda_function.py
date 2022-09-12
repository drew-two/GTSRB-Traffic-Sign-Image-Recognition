import os

import model

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'sign_predictions')
MODEL_NAME = os.getenv('MODEL_NAME')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'


model_service = model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    model_name=MODEL_NAME,
    test_run=TEST_RUN,
)


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    return model_service.lambda_handler(event)
