
variable "project_id" {
    description = "project_id"
    default = "mlops-final"
}

## AWS Variables
variable "aws_region" {
    description = "AWS region to create resources"
    default = "us-east-2"
}

variable "subnet_id" {
    description = "project_id"
}

variable "vpc_security_group_id" {
    description = "vpc_security_group_id"
}

variable "availability_zone" {
    description = "availability_zone"
}

## Resource parameters
variable "source_stream_name" {
    description = "Events sent to model"
}

variable "output_stream_name" {
    description = "Predictions from model"
}

variable "model_bucket_name" {
    description = "Model S3 bucket name"
}

variable "instance_type" {
    description = "General EC2 instance type"
}

variable "ami_id" {
    description = "General service AMI ID"
}

variable "mlflow_instance_name" {
    description = "MLflow instance name"
}

variable "train_instance_name" {
    description = "Training EC2 instance name"
}

variable "train_instance_type" {
    description = "Training EC2 instance type"
}

variable "train_ami_id" {
    description = "Training EC2 instance AMI to use"
}

variable "key_name" {
    description = "Key-value pair to use (should already exist in AWS)"
}

## Module variables

variable "lambda_function_local_path" {
    description = "Path to final lambda function"
}

variable "run_id" {
    description = "Run ID for model"
}

variable "docker_image_local_path" {
    description = "Path to dockerfile"
}

variable "ecr_repo_name" {
    description = "ECR repo name"
}

variable "lambda_function_name" {
    description = "Main lambda function name"
}