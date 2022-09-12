aws_region = "us-east-2"
subnet_id = "subnet-0f52ce138a72959bd"
vpc_security_group_id = "sg-091776d030c85068d"
availability_zone = "us-east-2a"
key_name = "MLOps"

source_stream_name = "sign_events"
output_stream_name = "sign_predictions"
model_bucket_name = "sign-predict-mlflow-models"
lambda_function_local_path = "../lambda_function.py"
docker_image_local_path = "../Dockerfile"
ecr_repo_name = "sign_prediction_model"
lambda_function_name = "sign_prediction_lambda"
model_name="sign-classifier"

instance_type = "t2.2xlarge"
train_instance_type = "p3.2xlarge"
train_ami_id = "ami-05cb80e877a1b315b"
