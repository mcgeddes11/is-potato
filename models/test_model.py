from models.models import IsPotatoModel
from PIL import Image
model = IsPotatoModel("classifier_model.h5", img_height=150, img_width=150)
image1 = Image.open("/app/static/potatoes/test.jpg")
image2 = Image.open("C:\\Projects\\code\\is-potato\\app\\static\\potatoes\\not_potato.jpg")

r1 = model.predict(image1)
r2 = model.predict(image2)

