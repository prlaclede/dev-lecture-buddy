import psycopg2, psycopg2.extras, time, os, datetime, logging
from flask import (Flask, render_template, request, 
session, url_for, redirect, send_from_directory)
from flask.ext.mail import Mail
from smtplib import SMTPException
from flask.ext.assets import Environment, Bundle
from flask.ext.iniconfig import INIConfig
from views import *
from modules import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

INIConfig(app)

app.config.from_inifile_sections('protected/config.ini', ['flask'])

app.register_blueprint(adminAPI)
app.register_blueprint(accountAPI)
app.register_blueprint(studentAPI)
app.register_blueprint(mailAPI)

assets = Environment(app)

pluginJS = Bundle('js/plugins/Chart.js/Chart.js', 'js/plugins/heatmap.js/heatmap.js', 
                    'js/plugins/jquery/jquery-1.12.0.min.js')
customJS = Bundle('js/custom/lb.js', 'js/custom/email.js')

pluginCSS = Bundle('css/plugins/default.css', 'css/plugins/fonts.css')

customCSS = Bundle('css/custom/lecturebuddy.css', 'css/custom/icons.css')

allJS = Bundle(pluginJS, customJS)

allCSS = Bundle(pluginCSS, customCSS)

assets.register('allJS', allJS)
assets.register('allCSS', allCSS)

