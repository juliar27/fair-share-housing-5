from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./ecoverde-master')

@app.route('/')
def show_home():
    return render_template('index.html')
