from flask import Flask, render_template
import os

homedir = "/opt/corona/app_corona"

os.chdir(homedir)

app = Flask(__name__, template_folder="plots")

@app.route("/")
def serve():
    return render_template("index_es.html")

@app.route("/<key>")
def serve_key(key):
    try:
        return render_template("{}".format(key))
    except:
        return "<h1>No plot to this shortcut available.</h1><h3>Available endpoints are:\n'{}'.</h3>".format("', '".join([os.path.splitext(n)[0] for n in os.listdir("plots")]))

app.run(host="0.0.0.0",port=5000,debug=True)
