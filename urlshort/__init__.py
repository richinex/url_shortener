from flask import Flask



def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'h5dshjd6dss5dsssdjfdd4ssf501ga43726dskjdsnakd'

    from . import urlshort
    # we then register urlshort into the application
    # also rename app.py to urlshort.py
    app.register_blueprint(urlshort.bp)
    return app
