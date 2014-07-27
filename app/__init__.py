import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from flask_debugtoolbar import DebugToolbarExtension

import config

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

print 'Flask app "%s" initialized' % __name__

app.secret_key = config.SECRET_KEY