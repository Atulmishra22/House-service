from flask import Flask
from backened.modals import db
from backened.api import *

app = None
def setup():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house_data.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.app_context().push()
    db.init_app(app)
    api.init_app(app)
    app.debug = True

setup()

from backened.controller import *



if __name__ == "__main__":
    app.run(debug=True)