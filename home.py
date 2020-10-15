from flask import Flask, render_template, request, make_response, redirect
from data.parse import parse_file, parse_address
from data.database import Database
# from form import LoginForm

app = Flask(__name__, template_folder='.')
app._static_folder = 'static'
app.config['SECRET_KEY'] = 'ausdhfaiuhvizizuhfsi'

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
    t = render_template('admin/dist/index.html', rows=rows)
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

@app.route('/header.html')
def show_header():
    t = render_template('site/header.html')
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

# @app.route('/add', methods=['GET', 'POST'])
# def show_add():
#     form = LoginForm()
#     t = render_template('admin/dist/add.html', form=form)
#     return make_response(t)

# @app.route('/added', methods = ['GET', 'POST'])
# def show_added():
#     if request.method == "POST":
#         form = request.form
#         record = {}
#         record['municode'] = form.get('municode')
#         record['municipality'] = form.get('municipality')
#         record['county'] = form.get('county')
#         record['region'] = form.get('region')
#         record['name'] = form.get('name')
#         record['developer'] = form.get('developer')
#         record['compliance'] = form.get('compliance')
#         record['address'] = parse_address(form.get('address'))
#         record['total'] = form.get('total')
#         record['family'] = form.get('family')
#         record['sr'] = form.get('senior')
#         record['famsale'] = form.get('famsale')
#         record['famrent'] = form.get('famrent')
#         record['srsale'] = form.get('srsale')
#         record['srrent'] = form.get('srrent')
#         record['ssn'] = form.get('ssn')
#         record['ssnsale'] = form.get('ssnsale')
#         record['ssnrent'] = form.get('ssnrent')
#         record['v1'] = form.get('v1')
#         record['v2'] = form.get('v2')
#         record['v3'] = form.get('v3')
#         record['vssn'] = form.get('vssn')
#         record['l1'] = form.get('l1')
#         record['l2'] = form.get('l2')
#         record['l3'] = form.get('l3')
#         record['lssn'] = form.get('lssn')
#         record['m1'] = form.get('m1')
#         record['m2'] = form.get('m2')
#         record['m3'] = form.get('m3')
#         record['mssn'] = form.get('mssn')
#         record['br1'] = form.get('br1')
#         record['br2'] = form.get('br2')
#         record['br3'] = form.get('br3')
#
#         deletelist = []
#         for column, value in record.items():
#             if value == '':
#                 deletelist.append(column)
#         for i in deletelist:
#             del record[i]
#
#         database = Database()
#         database.connect()
#         cursor = database._connection.cursor()
#         cursor.execute('SELECT listingid from listings')
#         row = cursor.fetchone()
#         new_id = 1
#         while row is not None:
#             if int(row[0]) >= new_id:
#                 new_id = int(row[0]) + 1
#             row = cursor.fetchone()
#         record['listingid'] = str(new_id)
#         database.add_record(record)
#         cursor.close()
#         database.disconnect()
#     t = render_template('admin/dist/uploaded.html')
#     return make_response(t)

if __name__ == "__main__":
    app.run(port=44424)
