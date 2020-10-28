from flask import Flask, render_template, request, make_response, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, make_secure_token, logout_user

from data.parse import parse_file, parse_address
from data.tables import get_tables, add_to_table, get_listings, get_row, edit_table, get_coords, edit_tables
from data.account import make_account, check_account
from data.database import Database
from data.download import download
from form import AddForm
from werkzeug.datastructures import MultiDict
from threading import Thread
from rq import Queue
from worker import conn

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
        # make_secure_token(self.email, key='secret_key')
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get(self):
        database = Database()
        database.connect()
        cursor = database._connection.cursor()
        query = "SELECT email from users where id = " + "'" + str(self) + "';;"
        cursor.execute(query)
        email = cursor.fetchone()
        database.disconnect()
        return User(email[0], self, True)


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
    rows, ids = get_listings()
    x = []
    for i in range(len(rows)):
        coords = rows[i][1].split(',')
        x.append([float(coords[0]), float(coords[1])])
#    x = [[40.0, 40.0], [40.9034902, -74.6402976], [41.0340749, -74.1058578], [40.90802130000001, -74.4261363], [40.895669, -74.16049199999999]]
#    ans = {}
#    for x in rows:
#        coords = x[1].split(',')
#        ans[coords[0]] = coords[1]
    t = render_template('site/map.html', ro=x)
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
    lid = request.args.get('id')
    adr = request.args.get('adr')
    coords = request.args.get('coords').split(',')
    lat = coords[0]
    long = coords[1]
    row = get_row(lid)
    t = render_template('site/details.html', row=row, adr=adr, lat=lat, long=long)
    return make_response(t)

#-----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def show_login():
    t = render_template('site/login.html')
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


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
    if request.method == "POST":
        if request.files['file'].filename != '':
            filename = request.files['file']

            flag, possible_redirect, changed_addresses = parse_file(filename)

            if not flag:
                return redirect(possible_redirect)
        else:
            return redirect("/upload-error")

    # thread = Thread(target=get_coords, args=(changed_addresses,))
    # thread.daemon = True
    # thread.start()
    q.enqueue(get_coords, changed_addresses)

    return redirect('/admin')

    # t = render_template('site/uploaded.html')
    # return redirect('/admin')


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

    database = Database()
    database.connect()
    database.clear()
    database.disconnect()
   # t = render_template('site/cleaned.html')


    return redirect('/admin')
# make_response(t)


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# @app.route('/add', methods=['GET', 'POST'])
# def show_add():

#     form = AddForm()
#     t = render_template('site/add.html', form=form)
#     return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------

@app.route('/edit', methods=['GET', 'POST'])
# def show_edit():
#     if request.method == 'GET':
#         print(request.args.get('id'))
#         record = get_row(request.args.get('id'))
#         form = AddForm(formdata=MultiDict(record))
#     else:
#         form = AddForm()
#     t = render_template('site/edit.html', form=form, id=request.args.get('id'))
#     return make_response(t)

def edit():

    if request.method == 'GET':
        return redirect('/tables')
    else:
        lookup = {0:'listingid', 1:'name', 2:'developer', 3:'status',
        4:'compliance', 5:'address', 6:'municipality', 7:'county', 8:'municode',
        9:'region', 10:'v1', 11:'v2', 12:'v3', 13:'l1', 14:'l2',
        15:'l3', 16:'m1', 17:'m2', 18:'m3', 19:'vssn', 20:'lssn', 21:'mssn',
        22:'famsale', 23:'famrent', 24:'srsale', 25:'srrent', 26:'ssnsale',
        27:'ssnrent', 28:'total', 29:'family', 30:'sr', 31: 'ssn',
        32:'br1', 33:'br2', 34:'br3'}
        form = request.form.to_dict()
        records = {}
        rows = get_tables()
        for item in form:
            current = item.split(';')
            value = form[item]
            if int(current[1]) > 9 and form[item] == 'None':
                value = '0'
            if int(current[0]) <= len(rows) and value == rows[int(current[0]) - 1][int(current[1])]:
                continue
            if not current[0] in records:
                records[current[0]] = {}
            records[current[0]][lookup[int(current[1])]] = value
        for record in records:
            edit_tables(records[record], record)
            
        return redirect('/tables')






# ----------------------------------------------------------------------------------------------------------------------
@app.route('/added', methods=['GET', 'POST'])
def show_added():

    if request.method == "POST":
        form = request.form
        add_to_table(form)
        #t = render_template('site/added.html')
        # return redirect('/admin')#make_response(t)

        return redirect('/admin')

    else:
        return redirect('/add')


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/edited', methods=['GET', 'POST'])
def show_edited():


    if request.method == "POST":
        form = request.form
        edit_table(form, request.args.get('id'))
        #t = render_template('site/edited.html')


        return redirect('/tables')
        #make_response(t)
    else:
        if request.args.get('id'):
            return redirect('/edit?id=' + request.args.get('id'))

        return redirect('/tables')


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/deleted', methods=['GET', 'POST'])
def show_deleted():

    if request.method == "POST":
        database = Database()
        database.connect()
        # print(request.args.get('id'))
        database.delete_record(request.args.get('id'))
        database.disconnect()
        #t = render_template('site/deleted.html')


        # return redirect('/tables')
        #make_response(t)
    # else:
    return redirect('/tables')


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/create', methods=['POST'])
def show_create():
    flag = make_account(request.form.to_dict())

    if not flag:
        t = render_template('site/used-email.html')
        return make_response(t)

    else:
        return redirect('/admin')
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
@app.route('/check', methods=['POST'])
def show_check():
    dict = request.form.to_dict()
    flag, unique_id = check_account(dict)

    if not flag:
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
    rows = get_tables()
    t = render_template('site/admin.html', rows=rows)
    return make_response(t)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=44434, debug=True)

# ----------------------------------------------------------------------------------------------------------------------
