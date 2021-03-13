import os

from flask import Flask, render_template, request, send_from_directory

from Utilities.patternRecognitionOCR import convert_toText

app = Flask(__name__)

app.config["CACHE_TYPE"] = "null"


UPLOAD_FOLDER = 'images'
CURR_DIRECTORY = os.getcwd()
UPLOAD_FOLDER_PATH = os.path.join(CURR_DIRECTORY,UPLOAD_FOLDER)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convertToText", methods=['POST'])
def convert_image_to_Text():

    pattern = request.form.get("regexSelect")
    textRegex = request.form.get("other")
    print(textRegex)
    uploaded_file = request.files['img']
    #filename = uploaded_file.filename
    path = UPLOAD_FOLDER_PATH + uploaded_file.filename

    uploaded_file.save(path)
    text, img = convert_toText(path, pattern, textRegex)
    filename = pattern + ".jpg"
    path = UPLOAD_FOLDER_PATH + uploaded_file.filename

    uploaded_file.save(path)


    return render_template("OCR_Converted_Text.html", Img_path=filename, Converted_text=text)
    return display_text


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run(port=4998, debug=True)
