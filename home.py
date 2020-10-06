from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

@app.route('/')
def show_home():
    return render_template('index.html')