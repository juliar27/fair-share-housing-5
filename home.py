from flask import Flask, render_template, request, make_response, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user
from py.parse import parse_file, parse_address
from py.account import make_account, check_account, account_get, authenticate, recovery, update_password
from py.database import Database, get_tables, add_to_table, get_listings, get_row, edit_table, get_coords, edit_tables, clear, delete, coords
from py.download import download
from py.form import AddForm
from werkzeug.datastructures import MultiDict
from threading import Thread
from rq import Queue
from py.worker import conn

# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__, template_folder='.')
app._static_folder = 'static'
app.config['SECRET_KEY'] = 'ausdhfaiuhvizizuhfsi'
q = Queue(connection=conn)
login = LoginManager(app)
login.login_view = "\login"


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
class User(UserMixin):
    def __init__(self, email, id, active=True):
        self.id = id
        self.email = email
        self.active = active

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get(self):
        email = account_get(self)
        return User(email, self, True)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@login.user_loader
def load_user(user_id):
    return User.get(user_id)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index')
def show_home():
    t = render_template('site/index.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/map')
def show_map():
    x, addressInfo = coords()
    t = render_template('site/map.html', ro=x, info=addressInfo)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/listings')
def show_listings():
    rows, ids = get_listings()
    t = render_template('site/listings.html', rows=rows, ids=ids)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/details')
def show_details():
    adr = request.args.get('adr')
    coords = request.args.get('coords').split(',')
    row = get_row(request.args.get('id'))
    t = render_template('site/details.html', row=row, adr=adr, lat=coords[0], long=coords[1])
    return make_response(t)

#-----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/password')
def show_password():
    t = render_template('site/password.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/register')
def show_register():
    t = render_template('site/register.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/tables')
def show_tables():
    rows = get_tables()
    t = render_template('site/tables.html', rows=rows)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/upload')
def show_upload():
    t = render_template('site/upload.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/parse-error')
def show_parse_error():
    insert = request.args.getlist('insert')
    col = request.args.getlist('col')
    rand = request.args.getlist('rand')
    t = render_template('site/parse-error.html', insert=insert, col=col, rand=rand)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/upload-error')
def show_upload_error():
    t = render_template('site/upload-error.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/uploaded', methods=['GET'])
def show_uploaded_get():
    return redirect('/upload')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/uploaded', methods=['POST'])
def show_uploaded_post():
    if request.files['file'].filename != '':
        flag, possible_redirect, changed_addresses = parse_file(request.files['file'])
        q.enqueue(get_coords, changed_addresses)

        if not flag:
            return redirect(possible_redirect)
    else:
        return redirect('/upload-error')


    return redirect('/admin')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/download')
def show_download():
    t = render_template('site/download.html')
    response = make_response(t)
    return response


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/downloaded', methods=['GET','POST'])
def show_downloaded():
    if request.method == "POST":
        download('out.xls')
        return send_file('out.xls', attachment_filename='listings.xls', as_attachment=True)
    else:
        return redirect('/download')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/clear', methods=['GET', 'POST'])
def show_clear():
    clear()
    return redirect('/admin')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if request.method == 'GET':
        return redirect('/tables')
    else:
        form = request.form.to_dict()
        edit(form)
        return redirect('/tables')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edited', methods=['GET', 'POST'])
def show_edited():
    if request.method == "POST":
        form = request.form
        edit_table(form, request.args.get('id'))
        return redirect('/tables')
    else:
        if request.args.get('id'):
            return redirect('/edit?id=' + request.args.get('id'))

        return redirect('/tables')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/added', methods=['GET', 'POST'])
def show_added():
    if request.method == "POST":
        form = request.form
        add_to_table(form)
        return redirect('/admin')
    else:
        return redirect('/add')
# ----------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------------------------
@app.route('/deleted', methods=['GET', 'POST'])
def show_deleted():
    if request.method == "POST":
        delete(request.args.get('id'))
    return redirect('/tables')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/verify', methods=['GET', 'POST'])
def show_verify():
    t = render_template('site/verify.html')
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/authenticate', methods=['GET', 'POST'])
def show_autheticate():
    id = request.args.get('id')
    authenticate(id)
    t = render_template('site/authenticate.html')
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/recovery', methods=['GET'])
def show_recovery():
    id = request.args.get('id')
    t = render_template('site/recovery.html', id=id)
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/newpassword', methods=['POST'])
def show_newpassword():
    update_password(request.form.to_dict())
    return redirect('/login')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/reset', methods=['POST'])
def show_reset():
    no_account = recovery(request.form.to_dict())
    # if no_account:
    return redirect('/login')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/create', methods=['POST'])
def show_create():
    flag = make_account(request.form.to_dict())

    if not flag:
        t = render_template('site/used-email.html')
        return make_response(t)

    else:
        return redirect('/verify')
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def show_login():
    t = render_template('site/login.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/check', methods=['POST'])
def show_check():
    dict = request.form.to_dict()
    flag, unique_id, verify = check_account(dict)

    if not flag and verify:
        return redirect('/verify')
    elif not flag:
        return redirect('/login')
    else:
        login_user(User(dict['inputEmailAddress'], unique_id))
        return redirect('/admin')

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['POST', 'GET'])
def show_logout():
    logout_user()
    return redirect('/admin')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/admin')
def show_admin():
    t = render_template('site/admin.html', rows=get_tables())
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=44434, debug=True)

# ----------------------------------------------------------------------------------------------------------------------
