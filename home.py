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

@app.route('/agent')
def show_agent():
    t = render_template('agent.html')
    return make_response(t)

@app.route('/blog')
def show_blog():
    t = render_template('blog.html')
    return make_response(t)

@app.route('/blog-single')
def show_blog_single():
    t = render_template('blog-single.html')
    return make_response(t)

@app.route('/contact')
def show_contact():
    t = render_template('contact.html')
    return make_response(t)

@app.route('/main')
def show_main():
    t = render_template('main.html')
    return make_response(t)

@app.route('/properties')
def show_props():
    t = render_template('properties.html')
    return make_response(t)

@app.route('/properties-single')
def show_props_single():
    t = render_template('properties-single.html')
    return make_response(t)

@app.route('/services')
def show_services():
    t = render_template('services.html')
    return make_response(t)

if __name__ "__main__":
    app.run(port=55555)