from flask import Flask, render_template, request, make_response, redirect, url_for, send_file, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from py.parse import parse_file, parse_address
from py.account import make_account, check_account, account_get, authenticate, recovery, update_password, valid_id
from py.favorites import get_favorite_listings
from py.download import download
from py.auth import Server
from py.query import filter_function, map_query, listings_query
from py.details import get_details, get_row
from py.admin import get_tables, edit_listings, delete, clear
from werkzeug.datastructures import MultiDict
from rq import Queue
from worker import conn
from datetime import timedelta
from urllib.parse import quote_plus

# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__, template_folder='.')
app._static_folder = 'static'
app.config['SECRET_KEY'] = 'ausdhfaiuhvizizuhfsi'
q = Queue(connection=conn)
login = LoginManager(app)
login.login_view = "\login"
server = Server()

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
    app.permanent_session_lifetime = timedelta(minutes=1440)
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
    x, addressInfo, counties, towns, rows, ids = map_query("none", "none", "none", "none", "none", "none", '')
    t = render_template('site/map.html', ro=x, info=addressInfo, counties=counties, towns=towns, det=rows)

    response = make_response(t)
    return response
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/map-filtering')
def show_map_filtering():
    owner = request.args.get('ownership')
    prop = request.args.get('property')
    bed = request.args.get('bedrooms')
    income = request.args.get('income')
    town = request.args.get('town')
    county = request.args.get('county')
    zipCode = request.args.get('zip')

    if owner is None:
        owner = "none"
    if prop is None:
        prop = "none"
    if bed is None:
        bed = "none"
    if income is None:
        income = "none"
    if town is None:
        town = "none"
    if county is None:
        county = "none"
    if zipCode is None:
        zipCode = ''

    x, addressInfo, counties, towns, rows, ids = map_query(owner, prop, bed, income, town, county, zipCode)
    y = jsonify([x, addressInfo, counties, towns, rows, ids])
    print(y)
    return make_response(y)
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
        town = "none"

    if request.args.get('county') is not None:
        county = request.args.get('county')
    else:
        county = "none"

    if request.args.get('zip') is not None:
        zipCode = request.args.get('zip')
    else:
        zipCode = ""

    filtered_rows, filtered_ids, counties, towns = listings_query(owner, prop, bed, income, town, county, zipCode)

    html = ''
    for i in range(len(filtered_rows)):
        html += '<tr><td><a href=\'details?id=' + str(filtered_ids[i]) + '&adr=' + str(quote_plus(filtered_rows[i][0])) + '\'' + 'target="_blank">' + str(filtered_rows[i][0]) + '</a></td>'
        for j in range(2, len(filtered_rows[i])):
            html += '<td>' + str(filtered_rows[i][j]) + '</td>'
        html += '</tr>'
    return make_response(html)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/listings')
def show_listings():
    filtered_rows, filtered_ids, counties, towns = listings_query("", "", "", "","none", "none", "")
    t = render_template('site/listings.html', rows=filtered_rows, ids=filtered_ids, counties=counties, towns=towns)
    response = make_response(t)
    return response


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/details')
def show_details():
    id = request.args.get('id')
    adr = request.args.get('adr')

    if id == '' or id == None or not id.isnumeric() or adr is None:
        t = render_template("site/404.html", where="listings", message="Return to Listings")
        return make_response(t)

    info = get_details(id, adr)

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
        t = render_template('site/upload.html')
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
@app.route('/parse-error')
def show_parse_error():
    if current_user.is_authenticated:
        missing_columns = request.args.getlist('missing_columns')
        missing_columns_type = request.args.getlist('missing_columns_type')
        wrongtype = request.args.getlist('wrongtype')
        wrongtype_expected = request.args.getlist('wrongtype_expected')

        if missing_columns != [] and wrongtype == []:
            t = render_template('site/parse-error.html', empty_excel=zip(missing_columns,missing_columns_type), empty=True)
        else:
            t = render_template('site/parse-error.html', empty_excel=[], missing_columns=zip(missing_columns,missing_columns_type), wrongtype=zip(wrongtype, wrongtype_expected))

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
        flag, possible_redirect, changed_addresses = parse_file(request.files['file'], q)
        

        if not flag:
            return possible_redirect

        return '/admin-parsed'
    else:
        '/login'


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
            edit_listings(to_add, q)
            for row in to_delete:
                delete(row)

            data = {'message': 'Created', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)
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
    account, verified = recovery(request.form.to_dict(), server)
    if not account and not verified:
        return '/error'
    elif account and not verified:
        return '/verify'
    else:
        return '/verifypassword'
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/create', methods=['POST'])
def show_create():
    flag = make_account(request.form.to_dict(), server)
    if not flag:
        return '/error'
    else:
        return '/verify'
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
@app.route('/admin-parsed')
def show_admin():
    if current_user.is_authenticated:
        t = render_template('site/admin.html', rows=get_tables(), parsed=True)
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/admin')
def show_admin():
    if current_user.is_authenticated:
        t = render_template('site/admin.html', rows=get_tables(), parsed=False)
        return make_response(t)
    else:
        return redirect('/login')


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=44134, debug=True)

# ----------------------------------------------------------------------------------------------------------------------
