
from flask import Flask
from flask import render_template
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route("/")
def display():
    return render_template('index.html')