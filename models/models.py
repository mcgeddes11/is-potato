from keras.models import load_model
from PIL import Image
import numpy
import logging


class IsPotatoModel:
    def __init__(self, path_to_model, img_height, img_width):
        self.model = load_model(path_to_model)
        self.model.make_predict_function()
        self.img_height = img_height
        self.img_width = img_width

    def predict(self, image_data: Image):
        # Do the preprocessing and get a result
        image_data = image_data.resize((self.img_height, self.img_width))
        image_data = numpy.array(image_data.copy()) / 255.0
        image_data = numpy.expand_dims(image_data, axis=0)
        result = self.model.predict(image_data)
        # TODO: calibrate this
        if result[0][0] >= 0.5:
            return {"class": "is potato", "probability": result[0][0]}
        elif 0.25 < result[0][0] < 0.5:
            return {"class": "is maybe potato", "probability": result[0][0]}
        else:
            return {"class": "is not potato", "probability": 1.0 - result[0][0]}


