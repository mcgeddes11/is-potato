from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        if 'imageFile' in request.files:
            # Image file uploaded
            image_file = request.files['imageFile']
            # Process the image file

        if 'imageUrl' in request.form:
            # Image URL pasted
            image_url = request.form['imageUrl']
            # Process the image URL

        return "Input received!"

    return render_template('ispotato_main.html', page_title="IsPotato?")


if __name__ == '__main__':
    app.run()
