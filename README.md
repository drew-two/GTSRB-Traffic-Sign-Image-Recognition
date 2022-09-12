# MLOps Final Project

## Dataset

Run the following to get the data if you need to train or something:

wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip
wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip

unzip -q ./data/GTSRB-Training_fixed.zip -d ../data
unzip -q ./data/GTSRB_Online-Test-Images-Sorted.zip -d ../data

rm -rf ./data/GTSRB/Online-Test-sort/Images

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
    3. terraform apply [--var-file=vars/stg.tfvars]
4. Connect to ports to see monitored services

Sorry... I didn't have time to make anything for you to test the lambda with. test/test_.py code might help

## Misc

- Integration tests are only partially complete (you can see the class code)
- Unit tests are done
- See pyproject.toml, .pre-commit-config.yaml for linter and/or code formatter
- There's pre-commit hooks
- MLflow tracking for experiment + models
    - See backend.db, ./models, or s3://mlops-final-models (public bucket)
    - There's only few runs in MLflow because I don't have the AWS quota to allocate GPU instances 
- Training instance (EC2)
- Kinesis streams
