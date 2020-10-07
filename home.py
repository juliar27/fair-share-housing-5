from flask import Flask, render_template, request, make_response

app = Flask(__name__, template_folder='site')
app._static_folder = 'static'

@app.route('/', methods=['GET'])
@app.route('/index')
def show_home():
    t = render_template('index.html')
    return make_response(t)

@app.route('/about')
def show_about():
    t = render_template('about.html')
    return make_response(t)

@app.route('/listings')
def show_listings():
    t = render_template('listings.html')
    return make_response(t)

@app.route('/admin')
def show_admin():
    t = render_template('admin.html')
    return make_response(t)

@app.route('/map')
def show_map():
    t = render_template('map.html')
    return make_response(t)

@app.route('/main')
def show_main():
    t = render_template('main.html')
    return make_response(t)

if __name__ == "__main__":
    app.run(port=55555)
