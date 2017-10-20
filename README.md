
#Deep Geoscience

Contributions: 
1. Pre-processed dataset of SAT6 to be compatible with Inception v3 repository
2. A high performance satellite image classification model

## System requirement
Python 3.6+
Tensorflow

## Steps to verify the model performance
* Assume to be in the project home directory
* Assume all the system requirements have been satisfied
1. Download SAT-6 dataset: [Download page](http://csc.lsu.edu/~saikat/deepsat/)
2. Preprocess SAT-6 dataset ```python data_loader/sat_loader.py```
3. Transfer-learning: 
```python image_retraining/retrain.py --image_dir SAT-4_and_SAT-6_datasets/inception_ready``` 

## File description
**ls_data_reader.py**
An extendable class whose objects can handle LandSat image data.
**sat_loader.py**
Script to pre-process SAT-6 dataset in .mat format

## Other stuff in this respository
### Inference using Inception v3 pre-trained by Google (Before transfer learning):
```python imagenet/classify_image.py --image_file <location/to/image/file>```

### Transfer-learning: Train Inception v3's final layer for new classification task

```python image_retraining/retrain.py --image_dir SAT-4_and_SAT-6_datasets/inception_ready ```

### Results: 
```
INFO:tensorflow:2017-10-20 13:56:32.604209: Step 3999: Train accuracy = 96.0%
INFO:tensorflow:2017-10-20 13:56:32.604325: Step 3999: Cross entropy = 0.131267
INFO:tensorflow:2017-10-20 13:56:32.733847: Step 3999: Validation accuracy = 98.0% (N=100)
INFO:tensorflow:Final test accuracy = 96.7% (N=40478)
```

Baseline: **"Deep-SAT"** on SAT-6 93.9%

##References:

[Inception V3 Inference](https://www.tensorflow.org/tutorials/image_recognition
)

[Retrain ImageNet for new categories](https://www.tensorflow.org/tutorials/image_retraining)


**Saikat Basu, Sangram Ganguly, Supratik Mukhopadhyay, Robert Dibiano, Manohar Karki and Ramakrishna Nemani**, DeepSat - A Learning framework for Satellite Imagery, ACM SIGSPATIAL 2015.

