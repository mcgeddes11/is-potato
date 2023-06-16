from flask import Flask, render_template, request, redirect, url_for
import requests
from PIL import Image
from io import BytesIO
from uuid import uuid4
from models import IsPotatoModel
import os
import json

model = IsPotatoModel(os.path.join(os.environ["MODEL_PATH"], "classifier_model.h5"),
                      img_width=150,
                      img_height=150)

# TODO: externalize this as a database of some kind
results_object = {}
results_object["test"] = {"class": "is potato", "probability": 1.0}

app = Flask(__name__)
# TODO: configure to auto-delete the static/imgs files that are older than x days

@app.route('/', methods=['GET'])
def landing_page():
    return render_template('ispotato_main.html', page_title="IsPotato?")

@app.route('/process', methods=["POST"])
def process_input():
    if request.method == 'POST':
        if 'imageFile' in request.files:
            # Image file uploaded
            image_file = request.files['imageFile']
            if image_file.content_length > 0:
                print("Received a file")
                # Process the image file

        if 'imageUrl' in request.form:
            # Image URL pasted
            image_url = request.form['imageUrl']
            response = requests.get(image_url)
            if response.status_code != 200 or "image" not in response.headers["Content-Type"]:
                print("bad file, not an image")
            else:
                image = Image.open(BytesIO(response.content))
                # process the image using our model
                # TODO: include logic to output potato/not potato in model class
                results = model.predict(image)
                # save to file?
                image_id = str(uuid4())
                results_object[image_id] = results
                image.save(os.path.join(app.root_path, "static", "potatoes", "{}.jpg".format(image_id)))

                return redirect(url_for("ispotato_results", id=image_id))
    else:
        render_template('ispotato_main.html', page_title="IsPotato?")


@app.route('/results/<id>')
def ispotato_results(id):
    result = results_object[id]
    return render_template('ispotato_results.html', id=id, ispotato=result["class"], confidence=result["probability"])

if __name__ == '__main__':
    app.run()
