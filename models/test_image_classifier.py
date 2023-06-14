# script to generate some results for the classifier using known, unseen data

from keras.models import load_model
import pandas

from keras.preprocessing.image import ImageDataGenerator

model = load_model("classifier_model.h5")

input_folder = 'C:\\Projects\\data\\is-potato\\test'

datagen = ImageDataGenerator(rescale=1./255)
predict_generator = datagen.flow_from_directory(
    input_folder,
    target_size=(150, 150),
    batch_size=1,
    class_mode='binary',
    shuffle=False)

filenames = predict_generator.filenames
nb_samples = len(filenames)

predict = model.predict_generator(predict_generator, steps=nb_samples, verbose=1, workers=2)

output = pandas.DataFrame(data=filenames, columns=["image_filename"])
# this assumes a decision boundary of 0.5 which may not be accurate/performant
output["class"] = (predict > 0.5).astype(int)
output["probability"] = predict
output.to_csv("test_image_classes.csv", index=False)
print(predict)