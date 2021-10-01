from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

import os
import cv2
import algorithms
import numpy as np


STATIC_DIR = os.path.abspath("static")

steganomachine = algorithms.SteganoImage()

app = Flask(__name__, static_folder=STATIC_DIR)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "img/favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cryptography")
def cryptography():
    return render_template("cryptography-page.html", title='Modified RC4')


@app.route("/steganography-image")
@cross_origin()
def steganography_image():
    return render_template("steganography-image-page.html", title='Steganography with LSB')

@app.route("/steganography-audio")
@cross_origin()
def steganography_audio():
    return render_template("steganography-audio-page.html", title='Steganography with LSB')

@app.route("/audio-steganography")
def audio_steganography():
    return render_template("audio-steganography-page.html",
                           title='Audio steganography with LSB')


@app.route("/execute", methods=["POST"])
@cross_origin()
def execute():
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"]
        return algorithms.ModifiedRC4Cipher(key_input=key).compute(text)
        
@app.route("/action", methods=["POST"])
@cross_origin()
def action():
    if request.method == "POST":
        state = request.form["state"]
        return "State : " + state

@app.route("/encode-image", methods=["POST"])
def encode_image():
    if request.method == "POST":
        file = request.files['stegofile']
        file2 = request.files['messagefile']
        
        npimg = np.fromfile(file, np.uint8)
        file = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        print(file)
        capacity = steganomachine.calculate_capacity(file)
        return "TRUE"


@app.route("/encode-audio", methods=["POST"])
@cross_origin()
def encode_audio():
    if request.method == "POST":
        file = request.files["stegofile"]
        filename = secure_filename(file.filename) # save file 
        filepath = os.path.join("./algorithms/sample", filename)
        file.save(filepath)

        audio_stego = algorithms.AudioStego(filepath)
        # audio_stego.encode()
        # return algorithms.ModifiedRC4Cipher(key_input=key).compute(file)
    return "TESDASA"


if __name__ == "__main__":
    app.run(debug=True)