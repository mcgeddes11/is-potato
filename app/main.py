from flask import Flask, render_template, request, redirect, url_for
import requests
from PIL import Image
from io import BytesIO
from uuid import uuid4
from models.models import IsPotatoModel
import os
import logging
import traceback

# todo: do this better so i can save img width/weight with the model
model = IsPotatoModel(os.environ["MODEL_PATH"],
                      img_width=300,
                      img_height=300)

# TODO: externalize this as a database of some kind
# TODO: configure to auto-delete the static/imgs files that are older than x days
results_object = {}
results_object["test"] = {"class": "is potato", "probability": 1.0}

app = Flask(__name__)


@app.route('/', methods=['GET'])
def landing_page():
    logging.info("Hit base page")
    return render_template('ispotato_main.html', page_title="IsPotato?")


@app.route('/process', methods=["POST"])
def process_input():
    if request.method == 'POST':
        if 'imageFile' in request.files:
            # Image file uploaded
            image_file = request.files['imageFile']
            if image_file.filename != '':
                image = Image.open(image_file.stream)
                results = model.predict(image)
                image_id = str(uuid4())
                results_object[image_id] = results
                image.save(os.path.join(app.root_path, "static", "potatoes", "{}.jpg".format(image_id)))
                return redirect(url_for("ispotato_results", image_id=image_id))

        if 'imageUrl' in request.form:
            # Image URL pasted
            image_url = request.form['imageUrl']
            response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
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

                return redirect(url_for("ispotato_results", image_id=image_id))
    else:
        render_template('ispotato_main.html', page_title="IsPotato?")


@app.route('/results/<image_id>')
def ispotato_results(image_id):
    result = results_object[image_id]
    return render_template('ispotato_results.html', image_id=image_id, ispotato=result["class"], confidence=result["probability"])


@app.errorhandler(500)
def handle_exception(e):
    # return a custom error page or message
    return render_template('500.html', stacktrace=traceback.format_exception(e.original_exception)), 500


if __name__ == '__main__':
    app.run()
