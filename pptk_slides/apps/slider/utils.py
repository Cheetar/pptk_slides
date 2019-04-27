import random

import numpy as np

import cv2
from keras.models import load_model


def is_image_funny(img_file):
    img = cv2.imread(img_file)
    img = cv2.resize(img, (300, 300))
    img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img = np.reshape(img, [1, 300, 300, 3])

    model = load_model("PPTK-CNN.h5")
    prob_funny = model.predict(img)
    return random.uniform(0, 1) < prob_funny


def download_image(path):
    pass
