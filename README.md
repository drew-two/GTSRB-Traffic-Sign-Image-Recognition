# MLOps Final Project

## Dataset

Run the following to get the data:

!wget -P ../data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip
!wget -P ../data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip
rm -rf ../data/GTSRB/Online-Test-sort/Images

## Running code

Note: This runs a Convolutional Neural Network that may take a a few minutes to predict or be expensive to allocate in AWS for training. Also, buckets have been left public for your convenience.

s3://mlops-final-models
s3://tf-state-mlops-final

//TODO
- Run Terraform to deploy model
OR
- Load container locally via make

## Misc

- MLflow tracking for experiment + models
    - See backend.db, ./models, or s3://mlops-final-models (public bucket)
- See pyproject.toml, .pre-commit-config.yaml for linter and/or code formatter
- There's pre-commit hooks
