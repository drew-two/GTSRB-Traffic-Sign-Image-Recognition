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
# deploy parameters should go in variables.tf
