# run.py
from application import create_app, db
from application import models
from flask_migrate import Migrate

import os

app = create_app()
migrate = Migrate(app, db)

from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True

API_IP = os.environ['API_IP']
API_PORTS = os.environ['API_PORT']

if __name__ == "__main__":
    app.run(host=API_IP, port=int(API_PORTS))
