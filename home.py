from flask import Flask, render_template, request, make_response, redirect
from data.parse import parse_file, parse_address
from data.tables import get_tables, add_to_table, get_listings
from data.account import make_account, check_account
from form import LoginForm

# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__, template_folder='.')
app._static_folder = 'static'
app.config['SECRET_KEY'] = 'ausdhfaiuhvizizuhfsi'


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index')
def show_home():
    t = render_template('site/index.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/about')
def show_about():
    t = render_template('site/about.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/map')
def show_map():
    t = render_template('site/map.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/listings')
def show_listings():
    rows = get_listings()
    t = render_template('site/listings.html', rows=rows)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login')
def show_login():
    t = render_template('admin/dist/login.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/password')
def show_password():
    t = render_template('admin/dist/password.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/register')
def show_register():
    t = render_template('admin/dist/register.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/tables')
def show_tables():
    rows = get_tables()
    t = render_template('admin/dist/tables.html', rows=rows)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/upload')
def show_upload():
    t = render_template('admin/dist/upload.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/parse-error')
def show_parse_error():
    errorMsg = request.args.get('errorMsg')
    t = render_template('admin/dist/parse-error.html', errorMsg=errorMsg)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/uploaded', methods=['GET', 'POST'])
def show_uploaded():
    if request.method == "POST":
        filename = request.files['file']
        flag, possible_redirect = parse_file(filename)

        if not flag:
            return redirect(possible_redirect)

    t = render_template('admin/dist/uploaded.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/add', methods=['GET', 'POST'])
def show_add():
    form = LoginForm()
    t = render_template('admin/dist/add.html', form=form)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/added', methods=['GET', 'POST'])
def show_added():
    if request.method == "POST":
        form = request.form
        add_to_table(form)
    t = render_template('admin/dist/uploaded.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/create', methods=['POST'])
def show_create():
    flag = make_account(request.form.to_dict())

    if not flag:
        t = render_template('admin/dist/used-email.html')
        return make_response(t)

    else:
        return show_admin()

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/check', methods=['POST'])
def show_check():
    flag = check_account(request.form.to_dict())

    if not flag:
        # error message needs to put here
        t = render_template('admin/dist/login.html')
        return make_response(t)

    else:
        return show_admin()


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/admin')
def show_admin():
    rows = get_tables()
    t = render_template('admin/dist/index.html', rows=rows)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=44424)
# ----------------------------------------------------------------------------------------------------------------------
