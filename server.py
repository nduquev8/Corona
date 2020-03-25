from flask import Flask, render_template
import os

homedir = "/opt/corona/app_corona"

os.chdir(homedir)

app = Flask(__name__, template_folder="plots")

@app.route("/")
def serve():
    return render_template("norm.html")

@app.route("/<key>")
def serve_key(key):
    try:
        return render_template("{}.html".format(key))
    except:
        return "<h1>No plot to this shortcut available.</h1><h3>You may try 'norm', 'raw' or a country name in connection with 'norm' or 'raw' eg 'switzerland_raw'</h3>"

app.run(host="0.0.0.0",port=5000)
