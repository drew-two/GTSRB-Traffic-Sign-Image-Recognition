# Make sure to create state bucket beforehand
terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket  = "tf-state-mlops-final"
    key     = "mlops-final.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}

provider "aws" {
    region = var.aws_region
}

data "aws_caller_identity" "current_identity" {}

# fetch account_id and save to local variables
locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}
# think of local variables just for one file; variables.tf for the whole project
# deploy parameters (docker image, run id etc) should go in variables.tf

# Events sent to model
module "source_kinesis_stream"  {
  source   = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name =  "${var.source_stream_name}_${var.project_id}"
  tags = var.project_id
}

# Predictions from model
module "output_kinesis_stream"  {
  source   = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name =  "${var.output_stream_name}_${var.project_id}"
  tags = var.project_id
}

# model bucket
module "s3_bucket"  {
  source      = "./modules/s3"
  bucket_name = "${var.model_bucket_name}-${var.project_id}"
}

# MLflow instance
module "mlflow_instance"  {
  source        = "./modules/mlflow_ec2"
  ami_id        = var.ami_id
  key_name      = var.key_name
  ec2_name      = "${var.instance_name}-${var.project_id}"
  instance_type = vars.instance_type
  model_bucket  = module.s3_bucket.id
}


# # Training instance
# module "train_instance"  {
#   source        = "./modules/train_ec2"
#   ami_id        = var.train_ami_id
#   key_name      = var.key_name
#   ec2_name      = "${var.train_instance_name}-${var.project_id}"
#   instance_type = vars.train_instance_type
#   mlflow_dns     = module.mlflow_instance.private_dns
# }

# image registry
module "ecr_image" {
   source = "./modules/ecr"
   ecr_repo_name = "${var.ecr_repo_name}_${var.project_id}"
   region = var.aws_region
   account_id = local.account_id
   lambda_function_local_path = var.lambda_function_local_path
   docker_image_local_path = var.docker_image_local_path
}

module "lambda_function" {
  source                = "./modules/deploy_lambda"
  image_uri             = module.ecr_image.image_uri
  lambda_function_name  = "${var.lambda_function_name}_${var.project_id}"
  model_bucket          = module.s3_bucket.id
  run_id                = var.run_id
  output_stream_name    = "${var.output_stream_name}-${var.project_id}"
  output_stream_arn     = module.output_kinesis_stream.stream_arn
  source_stream_name    = "${var.source_stream_name}-${var.project_id}"
  source_stream_arn     = module.source_kinesis_stream.stream_arn
}