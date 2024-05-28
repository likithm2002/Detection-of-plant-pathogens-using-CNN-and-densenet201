import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from lib_file import lib_path
import tensorflow as tf
from lib_file import lib_path
from tensorflow.keras.models import load_model


model = load_model("models/DenseNet201_model.h5", compile=False)


class_labels = ['Bacterial Spot', 'Black Mold',
                'Gray Spot', 'Late Blight', 'Health', 'Powdery Mildew']


def data_loading(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def display_image(input_image):
    plt.imshow(input_image)
    plt.title(label="Input Image\n", fontsize=15)
    plt.axis("off")
    # plt.show()


def image_preprocessing(input_image):
    image = cv2.resize(input_image, (128, 128), interpolation=cv2.INTER_CUBIC)
    image = image.astype(np.float32)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    return image


def model_prediction(input_image):
    prediction = model.predict(input_image, verbose=1)
    class_label = np.argmax(prediction)
    class_name = class_labels[class_label]
    probability = prediction[0][class_label]

    return class_label, class_name, probability


def tomatoLeafDiseasePrediction(user_input):

    image = data_loading(user_input)

    display_image(image)

    image = image_preprocessing(image)
    print(image.shape)

    class_label, class_name, probability = model_prediction(image)

    print(f"CLASS LABEL: {class_label}")
    print(f"CLASS NAME: {class_name}")
    print(f"PROBABILITY: {probability:.3f}%")

    for text in os.listdir("info"):
        label = text.split(".")[0]
        if label == class_name.lower():
            filepath = os.path.join("info", f"{label}.txt")
            with open(file=filepath, mode='r') as file:
                data = file.read()
                # print("data : ", data)
        else:
            continue

    return class_name, probability, data
