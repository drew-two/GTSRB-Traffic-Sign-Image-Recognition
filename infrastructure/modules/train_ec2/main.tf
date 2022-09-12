# Create Kinesis Data Stream

resource "aws_instance" "train_ec2" {
    name            = var.instance_name
    instance_type   = var.instance_type
    ami             = var.ami
    subnet_id       = var.subnet_id 
}

output "stream_arn" {
    value = aws_kinesis_stream.stream.arn
}

output "ec2_arn" {
    value = aws_instance.train_ec2.arn
}

output "ec2_arn" {
    value = aws_instance.train_ec2.public_ip
}