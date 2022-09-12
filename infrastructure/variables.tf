variable "aws_region" {
    description = "AWS region to create resources"
    default = "us-east-2"
}

variable "project_id" {
    description = "project_id"
    default = "mlops-final"
}

variable "source_stream_name" {
    description = ""
}

variable "output_stream_name" {
    description = ""
}

variable "bucket_name" {
    description = "Model S3 bucket name"
}