from sys import argv
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<b>Hello world!</b>'  

app.run(debug=True)