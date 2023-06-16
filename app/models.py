from keras.models import load_model
from PIL import Image
import numpy


class IsPotatoModel:
    def __init__(self, path_to_model, img_height, img_width):
        self.model = load_model(path_to_model)
        self.img_height = img_height
        self.img_width = img_width

    def predict(self, image_data: Image):
        # Do the preprocessing and get a result
        image_data = numpy.array(image_data) / 255
        image_data = numpy.resize(image_data, (self.img_height, self.img_width, 3))
        image_data = numpy.expand_dims(image_data, axis=0)
        result = self.model.predict(image_data)
        # TODO: calibrate this
        if result[0][0] > 0.1:
            return {"class": "is potato", "probability": result[0][0]}
        else:
            return {"class": "is not potato", "probability": result[0][0]}


