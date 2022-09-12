variable "instance_name" {
    type = string
    description = "MLflow EC2 name"
}

variable "instance_type" {
    type = string
    description = "EC2 Instance size/type"
}

variable "ami_id" {
    description = "AMI ID"
}

variable "key_name" {
    description = "SSH Key pair to use that already exists in AWS"
}

variable "model_bucket" {
    description = "SSH Key pair to use that already exists in AWS"
}

variable "subnet_id" {
    type = string
    description = "project_id"
}

variable "vpc_security_group_id" {
    type = string
    description = "vpc_security_group_id"
}

variable "availability_zone" {
    type = string
    description = "availability_zone"
}
