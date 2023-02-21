# Only for local testing - different nomenclature from ECR

LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=GTSRB-prediction:${LOCAL_TAG}
test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

build: quality_checks test
	sudo docker build -t ${LOCAL_IMAGE_NAME} .

integration_test: build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration-test/run.sh

setup:
	pipenv install --dev
	pre-commit install

dataset:
	wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip
	wget -P ./data https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip

	unzip -q ./data/GTSRB-Training_fixed.zip -d ../data
	unzip -q ./data/GTSRB_Online-Test-Images-Sorted.zip -d ../data

	rm -rf ./data/GTSRB/Online-Test-sort/Images
