variable "ec2_name" {
    type = string
    description = "Training EC2 name"
}

variable "instance_type" {
    type = string
    description = "EC2 Instance size/type"
    # default = "p3.2xlarge"
    default = "t2.xlarge"
}

variable "ami_id" {
  description = "AMI ID"
  default = "ami-05cb80e877a1b315b"
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
