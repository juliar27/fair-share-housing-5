from flask import Flask, render_template, request, make_response, redirect, url_for, send_file, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from py.parse import parse_file, parse_address
from py.account import make_account, check_account, account_get, authenticate, recovery, update_password, valid_id
from py.database import Database, get_tables, edit_listings, add_to_table, get_row, edit_table, get_coords, edit_tables, clear, delete, coords, get_favorite_listings, get_details
from py.download import download
from py.map import querying_location, filter_function, query2, query3, query, html_for_listings
from py.form import AddForm
from werkzeug.datastructures import MultiDict
from threading import Thread
from rq import Queue
from worker import conn
from datetime import timedelta

# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__, template_folder='.')
app._static_folder = 'static'
app.config['SECRET_KEY'] = 'ausdhfaiuhvizizuhfsi'
q = Queue(connection=conn)
login = LoginManager(app)
login.login_view = "\login"


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
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@login.user_loader
def load_user(user_id):
    return User.get(user_id)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    t = render_template("site/404.html", where="index", message="mapFSH")
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/accounterror', methods=['GET', 'POST'])
def show_account_error():
    errorMsg = request.args.get('errorMsg')
    ref = request.args.get('ref')
    ref_msg = request.args.get('ref_msg')
    t = render_template('site/accounterror.html', errorMsg=errorMsg, ref=ref, ref_msg=ref_msg)
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index')
def show_home():
    t = render_template('site/index.html')
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/filtering')
@app.route('/map')
def show_map():
    prevOwner = request.cookies.get('prevOwner')
    prevProp = request.cookies.get('prevProp')
    prevBed = request.cookies.get('prevBed')
    prevIncome = request.cookies.get('prevIncome')
    prevTown = request.cookies.get('prevTown')
    prevCounty = request.cookies.get('prevCounty')
    prevZip = request.cookies.get('prevZip')

    if prevOwner is None:
        prevOwner = "none"
    if prevProp is None:
        prevProp = 'none'
    if prevBed is None:
        prevBed = "none"
    if prevIncome is None:
        prevBed = "none"
    if prevTown is None:
        prevTown = ''
    if prevCounty is None:
        prevCounty = ''
    if prevZip is None:
        prevZip = ''

    owner = request.args.get('ownership')
    prop = request.args.get('property')
    bed = request.args.get('bedrooms')
    income = request.args.get('income')
    town = request.args.get('town')
    county = request.args.get('county')
    zipCode = request.args.get('zip')

    if owner is None:
        if prevOwner is None:
            owner = "none"
        else:
            owner = prevOwner
    if prop is None:
        if prevProp is None:
            prop = "none"
        else:
            prop = prevProp

    if bed is None:
        if prevBed is None:
            bed = "none"
        else:
            bed = prevBed

    if income is None:
        if prevIncome is None:
            income = "none"
        else:
            income = prevIncome

    if town is None:
        if prevTown is None:
            town = ''
        else:
            town = prevTown

    if county is None:
        if prevCounty is None:
            county = ''
        else:
            county = prevCounty

    if zipCode is None:
        if prevZip is None:
            zipCode = ''
        else:
            zipCode = prevZip

    rows,x, addressInfo = query(owner, prop, bed, income, town, county, zipCode)
    t = render_template('site/map.html', ro=x, info=addressInfo, det=rows, prevOwner=owner, prevProp=prop, prevBed=bed, prevIncome=income, prevTown=town, prevCounty=county, prevZip=zipCode)

    response = make_response(t)
    response.set_cookie('prevOwner', owner, expires=0)
    response.set_cookie('prevProp', prop, expires=0)
    response.set_cookie('prevBed', bed, expires=0)
    response.set_cookie('prevIncome', income, expires=0)
    response.set_cookie('prevTown', town, expires=0)
    response.set_cookie('prevCounty', county, expires=0)
    response.set_cookie('prevZip', zipCode, expires=0)

    return response
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/favorites')
def show_favorites():
    t = render_template('site/favorites.html')
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/getfavs', methods=['GET', 'POST'])
def get_favorites():
    if request.method == 'GET':
        return redirect('/favorites')
    else:
        favorites = request.json
        rows, ids = get_favorite_listings(favorites)
        out = [rows, ids]
        return jsonify(out = out)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/list-filtering')
def show_filtered_listings():

    if request.args.get('bedrooms') is not None:
        bed = request.args.get('bedrooms')
    else:
        bed = "none"

    if request.args.get('income') is not None:
        income = request.args.get('income')
    else:
        income = "none"

    if request.args.get('property') is not None:
        prop = request.args.get('property')
    else:
        prop = "none"

    if request.args.get('ownership') is not None:
        owner = request.args.get('ownership')
    else:
        owner = "none"

    if request.args.get('town') is not None:
        town = request.args.get('town')
    else:
        town = ""

    if request.args.get('county') is not None:
        county = request.args.get('county')
    else:
        county = ""

    if request.args.get('zip') is not None:
        zipCode = request.args.get('zip')
    else:
        zipCode = ""

    filtered_rows, filtered_ids, county, town = query2(owner, prop, bed, income, town, county, zipCode)

    html = html_for_listings(filtered_rows, filtered_ids)
    return make_response(html)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/listings')
def show_listings():
    filtered_rows, filtered_ids, county, town = query2("", "", "", "", "", "", "")
    t = render_template('site/listings.html', rows=filtered_rows, ids=filtered_ids)
    response = make_response(t)
    return response


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/details')
def show_details():
    id = request.args.get('id')

    if id == '' or id == None or not id.isnumeric():
        t = render_template("site/404.html", where="listings", message="Return to Listings")
        return make_response(t)

    info = get_details(id)

    if type(info) == str:
        t = render_template("site/404.html", where="listings", message="Return to Listings")
        return make_response(t)

    coords = info[1].split(',')
    t = render_template('site/details.html', row=get_row(id), adr=info[0], lat=coords[0], long=coords[1])
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
    if current_user.is_authenticated:
        rows = get_tables()
        t = render_template('site/tables.html', rows=rows)
        return make_response(t)
    else:
        return redirect('/login')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/upload')
def show_upload():
    if current_user.is_authenticated:
        if request.args.get('error') is None:
            t = render_template('site/upload.html', error='')
        else:
            t = render_template('site/upload.html', error=request.args.get('error'))
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/parse-error')
def show_parse_error():
    if current_user.is_authenticated:
        insert = request.args.getlist('insert')
        col = request.args.getlist('col')
        rand = request.args.getlist('rand')
        exp = request.args.getlist('exp')

        if rand != []:
            t = render_template('site/parse-error.html', insert=insert, col=col, rand=zip(rand,exp), flag=True)
        else:
            t = render_template('site/parse-error.html', insert=insert, col=zip(col,exp), rand=exp, flag=False)

        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/uploaded', methods=['GET'])
def show_uploaded_get():
    if current_user.is_authenticated:
        return redirect('/upload')
    else:
        return redirect('/login')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/uploaded', methods=['POST'])
def show_uploaded_post():
    if current_user.is_authenticated:
        if request.files['file'].filename != '':
            flag, possible_redirect, changed_addresses = parse_file(request.files['file'])
            # q.enqueue(get_coords, changed_addresses)

            if not flag:
                return redirect(possible_redirect)
        else:
            return redirect(url_for('show_upload', error="T."))

        return redirect('/admin')
    else:
        redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/download')
def show_download():
    if current_user.is_authenticated:
        t = render_template('site/download.html')
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/downloaded', methods=['GET','POST'])
def show_downloaded():
    if current_user.is_authenticated:
        if request.method == "POST":
            download('out.xls')
            return send_file('out.xls', attachment_filename='listings.xls', as_attachment=True)
        else:
            return redirect('/download')
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/clear', methods=['GET', 'POST'])
def show_clear():
    if current_user.is_authenticated:
        clear()
        return redirect('/admin')
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if current_user.is_authenticated:
        if request.method == 'GET':
            return redirect('/tables')
        else:
            out = request.json
            to_add = out['to_add']
            to_delete = out['to_delete']
            edit_listings(to_add)
            for row in to_delete:
                delete(row)

            data = {'message': 'Created', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)
    else:
        return redirect('/login')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edited', methods=['GET', 'POST'])
def show_edited():
    if current_user.is_authenticated:
        if request.method == "POST":
            form = request.form
            edit_table(form, request.args.get('id'))
            return redirect('/tables')
        else:
            if request.args.get('id'):
                return redirect('/edit?id=' + request.args.get('id'))

            return redirect('/tables')
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/added', methods=['GET', 'POST'])
def show_added():
    if current_user.is_authenticated:
        if request.method == "POST":
            form = request.form
            add_to_table(form)
            return redirect('/admin')
        else:
            return redirect('/add')
    else:
        return redirect('/login')
# ----------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------------------------
@app.route('/deleted', methods=['GET', 'POST'])
def show_deleted():
    if current_user.is_authenticated:
        if request.method == "POST":
            delete(request.args.get('id'))
        return redirect('/tables')
    else:
        return redirect('/login')
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
    flag = authenticate(id)
    if not flag:
        return redirect(url_for('show_account_error', errorMsg="Something went wrong.", ref="login", ref_msg="Would you like to login?"))

    t = render_template('site/authenticate.html')
    return make_response(t)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/recovery', methods=['GET'])
def show_recovery():
    id = request.args.get('id')
    if valid_id(id):
        t = render_template('site/recovery.html', id=id)
        return make_response(t)
    else:
        return redirect(url_for('show_account_error', errorMsg="This URL has expired.", ref="password", ref_msg="Would you still like to reset your password?"))


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/verifypassword', methods=['GET'])
def show_verifypassword():
    t = render_template('site/verifypassword.html')
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
    account, verified = recovery(request.form.to_dict())
    if not account and not verified:
        return redirect(url_for('show_account_error', errorMsg="You do not have an account associated with this email.", ref="register", ref_msg="Would you like to create an account?"))

    elif account and not verified:
        return redirect('/verify')
    else:
        return redirect('/verifypassword')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/create', methods=['POST'])
def show_create():
    flag = make_account(request.form.to_dict())

    if not flag:
        return redirect(url_for('show_account_error', errorMsg="This email is already in-use.", ref="password", ref_msg="Did you forget your password?"))

    else:
        return redirect('/verify')
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def show_login():
    if current_user.is_authenticated:
        return redirect('/admin')
    else:
        t = render_template('site/login.html')
        return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/check', methods=['POST'])
def show_check():
    dict = request.form.to_dict()
    flag, unique_id, verify = check_account(dict)

    if not flag and verify:
        return '/verify'
    elif not flag:
        return '/login'
    else:
        login_user(User(dict['inputEmailAddress'], unique_id))
        return '/admin'

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/logout', methods = ['POST', 'GET'])
def show_logout():
    logout_user()
    return redirect('/login')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/admin')
def show_admin():
    if current_user.is_authenticated:
        t = render_template('site/admin.html', rows=get_tables())
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=44234, debug=True)

# ----------------------------------------------------------------------------------------------------------------------
