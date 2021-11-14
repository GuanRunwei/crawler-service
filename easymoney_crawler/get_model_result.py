import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as dataset

from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow
from torchvision import models
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from collections import defaultdict
from django.http import JsonResponse

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(),
    transforms.ToTensor()
])

VGG_model_path = "./deep learning model/CNN/VGG_model_lung_canc.pt"
resnet_model_path = "./deep learning model/CNN/resnet_model_lung_canc.pt"
desnet_model_path = "./deep learning model/CNN/desnet_model_lung_canc.pt"

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def get_CNN_result(request):
    try:
        image_path = request.GET["image_path"]
        result = ensemble_predict(image_path)
    except:
        return JsonResponse({"code": 400, "data": "error"})
    return JsonResponse({"code": 200, "data": result})


def ensemble_predict(image_path):
    image_lung = Image.open(image_path)

    cancer_categories = defaultdict(int)

    VGG_MODEL = torch.load(VGG_model_path, map_location='cpu')
    RESNET_MODEL = torch.load(resnet_model_path, map_location='cpu')
    DESNET_MODEL = torch.load(desnet_model_path, map_location='cpu')

    image_tensor = transform(image_lung)
    image_tensor = torch.unsqueeze(image_tensor, 0)
    image_tensor = image_tensor.to(device)
    # print(image_tensor.shape)

    output_VGG = VGG_MODEL(image_tensor)
    output_RESNET = RESNET_MODEL(image_tensor)
    output_DESNET = DESNET_MODEL(image_tensor)
    ensemble_results = [output_VGG[0], output_RESNET[0], output_DESNET[0]]
    print("VGGNET predict：", output_VGG)
    print("RESNET predict：", output_RESNET)
    print("DESNET predict：", output_DESNET)

    for item in ensemble_results:
        item = item.tolist()
        if item.index(max(item)) == 0:
            cancer_categories["lung_aca"] += 1
        else:
            if item.index(max(item)) == 1:
                cancer_categories["lung_n"] += 1
            else:
                cancer_categories["lung_scc"] += 1
    print("The vote result from 3 models：", cancer_categories)
    return max(cancer_categories, key=cancer_categories.get)


def keras_image_to_tensor(image_path):
  keras_image = image.load_img(image_path, target_size=(299, 299), color_mode='rgb')
  keras_image_tensor = image.img_to_array(keras_image)*(1.0/255.0)
  keras_image_tensor = np.asarray(torch.unsqueeze(torch.tensor(keras_image_tensor), 0))
  return keras_image_tensor


def keras_ensemble_predict(image_path):
    vgg_path = "./deep learning model/CNN/keras_vgg_weights.h5"
    inception_path = "./deep learning model/CNN/keras_inception_resnet_v2_weights.h5"
    resnet_path = "./deep learning model/CNN/keras_resnet_weights.h5"

    vgg = keras.models.load_model(vgg_path)
    inception = keras.models.load_model(inception_path)
    resnet = keras.models.load_model(resnet_path)

    vgg_result = vgg.predict(keras_image_to_tensor(image_path), batch_size=4)
    inception_result = inception.predict(keras_image_to_tensor(image_path), batch_size=4)
    resnet_result = resnet.predict(keras_image_to_tensor(image_path), batch_size=4)

    vote_result = np.argmax([str([torch.argmax(vgg_result[0]), torch.argmax(inception_result[0]), torch.argmax(resnet_result[0])]).count('0'), str([torch.argmax(vgg_result[0]), torch.argmax(inception_result[0]), torch.argmax(resnet_result[0])]).count('1'), str([torch.argmax(vgg_result[0]), torch.argmax(inception_result[0]), torch.argmax(resnet_result[0])]).count('2')])

    if vote_result == 0:
        return 'lung_aca'
    else:
        if vote_result == 1:
            return 'lung_n'
    return 'lung_scc'


def get_keras_CNN_result(request):
    try:
        image_path = request.GET["image_path"]
        result = keras_ensemble_predict(image_path)
    except:
        return JsonResponse({"code": 400, "data": "error"})
    return JsonResponse({"code": 200, "data": result})