variable "instance_type" {
    type = string
    description = "EC2 Instance size/type"
    default = "p3.2xlarge"
}

variable "availability_zone" {
    type = string
    description = ""
    default = "${var.aws_region}a"
}