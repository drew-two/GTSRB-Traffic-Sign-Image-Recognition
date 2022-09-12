# Create Kinesis Data Stream

resource "aws_instance" "train_ec2" {
    instance_type   = var.instance_type
    key_name        = var.key_name
    ami             = var.ami
    subnet_id       = var.subnet_id 

  tags = {
    Name = var.instance_name
  }

  provisioner "remote-exec" {
    inline = [
        "apt update",
        "echo \"export MLFLOW_URL=${var.mlflow_dns}\" >> ~/.bashrc",
        "git clone https://github.com/drew-two/MLOpsFinal.git",
        "cd MLOpsFinal/",
        "wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip",
        "wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip",
        "unzip -q ./data/GTSRB-Training_fixed.zip -d ../data",
        "unzip -q ./data/GTSRB_Online-Test-Images-Sorted.zip -d ../data",
        "rm -rf ./data/GTSRB/Online-Test-sort/Images"
    ]
  }
}   

output "ec2_arn" {
    value = aws_instance.train_ec2.arn
}

output "ec2_public_dns" {
    value = aws_instance.train_ec2._public_dns
}

output "ec2_private_dns" {
    value = aws_instance.train_ec2._private_dns
}