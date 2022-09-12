# MLOps Final Project

## Dataset

Run the following to get the data:

!wget -P ../data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip
!wget -P ../data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip
rm -rf ../data/GTSRB/Online-Test-sort/Images

## Running code

Note: This runs a Convolutional Neural Network that may take a a few minutes to predict or be expensive to allocate in AWS for training. Feel free to edit or dry run as you see fit to avoid costs...

Also, buckets have been left public for your convenience.

s3://mlops-final-models
s3://tf-state-mlops-final

### Terraform

0. Make sure you have a VPC with the appropriate permissions (like how we made in the course, able to use remote VS code, forward ports 4200, 5000 etc.) and your `aws configure` is set
1. cd to infrastructure/
3. Edit infrastructure/variables.tf as per your VPC
3. Run the terraform commands:
    1. terraform init
    2. terraform plan (optional: -out)
    3. terraform apply
4. Connect ports to see monitored services

## Misc

- MLflow tracking for experiment + models
    - See backend.db, ./models, or s3://mlops-final-models (public bucket)
    - There's only few runs in MLflow because I don't have the AWS quota to allocate GPU instances 
- See pyproject.toml, .pre-commit-config.yaml for linter and/or code formatter
- There's pre-commit hooks