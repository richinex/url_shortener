from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

# session allows us use cookies

# allows us to securely send msgs back n forth from the user
# to make sure those trying to snoop in on the connection cannot see the information


# breaking things into blue prints
# we then remove import flask
bp = Blueprint('urlshort', __name__)


# a route says whenever someone visits this web page, return back the following
# we also specify which url we wanna create a route for. '/' is base url
# rename every instance of app to bo and home to urlshort.home
@bp.route('/')
def home():
    return render_template('home.html', codes = session.keys())

#name of function and route do not have to match
@bp.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/app/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}




        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            # we also wanna save this into a cookies
            # you could save the assignment to a timestamp
            # we display the session in the homepage
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        # redirect to homepage. pass the function as argument
        return redirect(url_for('urlshort.home'))

# new route
# look for any sort od string after the first slash, any sort of string
# inputed into a variable called code
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            #  lets see if we can find the bproprate key we are looking for
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    # if the code matches we display the url back to the user
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))

    # return custom error message if the url provided doesnt exists
    return abort(404)

# customize error
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


## route for an api
@bp.route('/api')
def session_api():
    # we just need to back the session keys in a list and make
    # sure that its in a json format
    # flask uses jsonify to convert any list or dictionary into a json code
    return jsonify(list(session.keys()))
