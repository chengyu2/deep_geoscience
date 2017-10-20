
#Deep Geoscience


##ls_data_reader.py
An extendable class whose objects can handle LandSat image data.

##Inference using Inception v3 pre-trained by Google:
python imagenet/classify_image.py --image_file <location/to/image/file>

##Train Inception v3's final layer for new classification task

python image_retraining/retrain.py --image_dir /Users/chengyu/PycharmProjects/deep_geoscience/SAT-4_and_SAT-6_datasets/inception_ready 

### Results: Beating benchmark "Deep-SAT" from NASA (93.9%)
INFO:tensorflow:2017-10-20 13:56:32.604209: Step 3999: Train accuracy = 96.0%
INFO:tensorflow:2017-10-20 13:56:32.604325: Step 3999: Cross entropy = 0.131267
INFO:tensorflow:2017-10-20 13:56:32.733847: Step 3999: Validation accuracy = 98.0% (N=100)
INFO:tensorflow:Final test accuracy = 96.7% (N=40478)


Reference:

Inception V3 Inference
https://www.tensorflow.org/tutorials/image_recognition

Retrain ImageNet for new categories
https://www.tensorflow.org/tutorials/image_retraining

Deep-SAT
Saikat Basu, Sangram Ganguly, Supratik Mukhopadhyay, Robert Dibiano, Manohar Karki and Ramakrishna Nemani, DeepSat - A Learning framework for Satellite Imagery, ACM SIGSPATIAL 2015.



