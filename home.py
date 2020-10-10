from flask import Flask, render_template, request, make_response
from data.parse import parse_file

app = Flask(__name__, template_folder='.')
app._static_folder = 'static'

@app.route('/', methods=['GET'])
@app.route('/index')


def show_home():
    t = render_template('site/index.html')
    return make_response(t)

@app.route('/about')
def show_about():
    t = render_template('site/about.html')
    return make_response(t)

@app.route('/listings')
def show_listings():
    t = render_template('site/listings.html')
    return make_response(t)

@app.route('/login')
def show_login():
    t = render_template('admin/dist/login.html')
    return make_response(t)

@app.route('/admin')
def show_admin():
    t = render_template('admin/dist/index.html')
    return make_response(t)

@app.route('/password')
def show_password():
    t = render_template('admin/dist/password.html')
    return make_response(t)

@app.route('/register')
def show_register():
    t = render_template('admin/dist/register.html')
    return make_response(t)

@app.route('/tables')
def show_tables():
    t = render_template('admin/dist/tables.html')
    return make_response(t)

@app.route('/map')
def show_map():
    t = render_template('site/map.html')
    return make_response(t)

@app.route('/upload')
def show_upload():
    t = render_template('admin/dist/upload.html')
    return make_response(t)

@app.route('/uploaded', methods = ['GET', 'POST'])
def show_uploaded():
    if request.method == "POST":
        filename = request.files['file']
        parse_file(filename)
    t = render_template('admin/dist/uploaded.html')
    return make_response(t)

@app.route('/edit')
def show_edit():
    t = render_template('admin/dist/edit.html')
    return make_response(t)

if __name__ == "__main__":
    app.run(port=44440)
