# Project Statement

Between 20-50 million people are injured each year in traffic accidents and over 1 million die. These are now the global killers over individules ages 5-29. We have technology, Advanced Driving-Assistance Systems that are intended to aid drivers and improve safety. ADAS are an essential component of autonomous vehicles, and to that end, traffic sign recognition is a pertinent problem. Such systems can allow the vehicle to detect and recognize traffic signs in every direction, especially when drivers may not. The faster the rdetection and classification, especially compared to human reaction time, the greater the possible safety advantage granted to the driver.

To this end, sophisticated traffic sign classification systems are a necessary component of any ADAS system. This project will implement a toy example using a Convolutional Neural Network via Keras with the German Traffic Sign Recognition Benchmark (GTSRB). Although this is not ideal for a production vehicle, such applications could be useful for model testing by data scientists, or for monitoring production models as well as possible redundancy.

Chosen because I am interested and it is relatively small, should be easier to download/unpack etc.

Disclaimer: I trained this locally, as I have a GPU and Amazon GPU instances can be expensive.
Otherwise, I would have run that part in the cloud.

## Dataset:

German Traffic Sign Recognition Benchmark (GTSRB)
https://benchmark.ini.rub.de/

(Training Data)[https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip]

(Testing Data)[https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Online-Test-Images-Sorted.zip]

From Kaggle:

The German Traffic Sign Benchmark is a multi-class, single-image classification challenge held at the International Joint Conference on Neural Networks (IJCNN) 2011. We cordially invite researchers from relevant fields to participate: The competition is designed to allow for participation without special domain knowledge. Our benchmark has the following properties:

	- Single-image, multi-class classification problem
	- More than 40 classes
	- Large, lifelike database
	- More than 50,000 images in total
