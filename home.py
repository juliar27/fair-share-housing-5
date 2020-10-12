from flask import Flask, render_template, request, make_response, redirect
from data.parse import parse_file
from data.database import Database

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
    database = Database()
    database.connect()
    rows = database.get_rows()
    t = render_template('admin/dist/index.php', rows=rows)
    database.disconnect()
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
    database = Database()
    database.connect()
    rows = database.get_rows()
    t = render_template('admin/dist/tables.html', rows=rows)
    database.disconnect()
    return make_response(t)

@app.route('/map')
def show_map():
    t = render_template('site/map.html')
    return make_response(t)

@app.route('/upload')
def show_upload():
    t = render_template('admin/dist/upload.html')
    return make_response(t)

@app.route('/parse-error')
def show_parseerror():
    errorMsg = request.args.get('errorMsg')
    t = render_template('admin/dist/parse-error.html', errorMsg=errorMsg)
    return make_response(t)

@app.route('/uploaded', methods = ['GET', 'POST'])
def show_uploaded():
    if request.method == "POST":
        filename = request.files['file']
        flag, possible_redirect = parse_file(filename)

        if flag == False:
            return redirect(possible_redirect)

    t = render_template('admin/dist/uploaded.html')
    return make_response(t)

@app.route('/edit')
def show_edit():
    t = render_template('admin/dist/edit.html')
    return make_response(t)

if __name__ == "__main__":
    app.run(port=44424)
