# USAGE
# python test.py --images dataset/covid --model covid19.model
# python load_model.py --images malaria/testing --model saved_model.model
# import tensorflow.compat.v1 as tf

# import the necessary packages
import os

# from django.conf import settings
import sys

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import random
import cv2
# print(os.path.dirname())

model = load_model(os.path.join(sys.path[0], 'covid19.model'))
print(model)

# grab all image paths in the input directory and randomly sample them


# initialize our list of results
results = []


def test_covid(image_loc):
    imagePaths = list(paths.list_images(image_loc))
    random.shuffle(imagePaths)
    imagePaths = imagePaths[:16]
    # loop over our sampled image paths
    for p in imagePaths:
        # load our original input image
        orig = cv2.imread(p)

        # pre-process our image by converting it from BGR to RGB channel
        # ordering (since our Keras mdoel was trained on RGB ordering),
        # resize it to 64x64 pixels, and then scale the pixel intensities
        # to the range [0, 1]
        image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = image.astype("float") / 255.0

        # order channel dimensions (channels-first or channels-last)
        # depending on our Keras backend, then add a batch dimension to
        # the image
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        # make predictions on the input image
        pred = model.predict(image)
        pred = pred.argmax(axis=1)[0]

        # an index of zero is the 'parasitized' label while an index of
        # one is the 'uninfected' label
        label = "Covid" if pred == 0 else "Normal"
        color = (0, 0, 255) if pred == 0 else (0, 255, 0)
        print("---",label,"***")
        return label


if __name__ == '__main__':
    cmdargs = sys.argv
    # print("Args list: %s " % cmdargs)
    test_covid(cmdargs[1])
