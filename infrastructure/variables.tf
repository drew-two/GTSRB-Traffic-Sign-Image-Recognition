variable "aws_region" {
    description = "AWS region to create resources"
    default = "us-east-2"
}

variable "project_id" {
    description = "project_id"
    default = "mlops-final"
}

variable "subnet_id" {
    description = "project_id"
    default = "subnet-0f52ce138a72959bd"
}

variable "vpc_security_group_id" {
    description = "vpc_security_group_id"
    default = "sg-091776d030c85068d"
}

variable "availability_zone" {
    type = string
    description = ""
    default = "${var.aws_region}a"
}

variable "source_stream_name" {
    description = "Events sent to model"
}

variable "output_stream_name" {
    description = "Predictions from model"
}

variable "training_instance_name" {
    description = "Training EC2 server"
}

variable "model_bucket_name" {
    description = "Model S3 bucket name"
}