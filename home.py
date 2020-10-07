from flask import Flask, render_template, request, make_response

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

@app.route('/401')
def show_401():
    t = render_template('admin/dist/401.html')
    return make_response(t)

@app.route('/404')
def show_404():
    t = render_template('admin/dist/404.html')
    return make_response(t)

@app.route('/500')
def show_500():
    t = render_template('admin/dist/500.html')
    return make_response(t)

@app.route('/layout-static')
def show_static():
    t = render_template('admin/dist/layout-static.html')
    return make_response(t)

@app.route('/layout-sidenav-light')
def show_sidenav():
    t = render_template('admin/dist/layout-sidenav-light.html')
    return make_response(t)

@app.route('/charts')
def show_charts():
    t = render_template('admin/dist/charts.html')
    return make_response(t)


@app.route('/tables')
def show_tables():
    t = render_template('admin/dist/tables.html')
    return make_response(t)

@app.route('/map')
def show_map():
    t = render_template('site/map.html')
    return make_response(t)

@app.route('/main')
def show_main():
    t = render_template('main.html')
    return make_response(t)

if __name__ == "__main__":
    app.run(port=55535)
