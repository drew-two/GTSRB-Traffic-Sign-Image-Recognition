# Create Kinesis Data Stream

resource "aws_instance" "mlflow_ec2" {
    name            = var.instance_name
    instance_type   = var.instance_type
    security_groups = var.vpc_security_group_id
    key_name        = var.key_name
    ami             = var.ami_id
    subnet_id       = var.subnet_id 

  provisioner "remote-exec" {
    inline = [
        "echo \"export MODEL_BUCKET=${var.model_bucket}\" >> ~/.bashrc",
        "apt update",
        "aws s3 sync s3://mlops-final-models s3://$MODEL_BUCKET",
        "git clone https://github.com/drew-two/MLOpsFinal.git",
        "cd MLOpsFinal/",
        "screen -d -m mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root $MODEL_BUCKET"
    ]
  }
}

output "ec2_arn" {
    value = aws_instance.mlflow_ec2.arn
}

output "ec2_public_dns" {
    value = aws_instance.mlflow_ec2._public_dns
}

output "ec2_private_dns" {
    value = aws_instance.mlflow_ec2._private_dns
}