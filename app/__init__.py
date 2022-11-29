from flask import Flask
from app import views, models
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

