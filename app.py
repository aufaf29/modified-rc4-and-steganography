from flask import Flask, render_template, request, send_from_directory
import os

import algorithms

STATIC_DIR = os.path.abspath("static")

app = Flask(__name__, static_folder=STATIC_DIR)


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


@app.route("/steganography")
def steganography():
    return render_template("steganography-page.html",
                           title='Steganography with LSB')


@app.route("/audio-steganography")
def audio_steganography():
    return render_template("audio-steganography-page.html",
                           title='Audio steganography with LSB')


@app.route("/execute", methods=["POST"])
def execute():
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"]
        return algorithms.ModifiedRC4Cipher(key_input=key).compute(text)


@app.route("/action", methods=["POST"])
def action():
    if request.method == "POST":
        state = request.form["state"]
        return "State : " + state


if __name__ == "__main__":
    app.run(debug=True)