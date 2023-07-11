from flask import Flask, g 
from utils.db import db
import os 
import tempfile

app = Flask(__name__)

app.secret_key = 'aGFja2VhYmxl' # base64
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/masiveMailer'
app.config['SQLALCHEMY_TRACKS_MODICATIONS'] = False
db.init_app(app)

## Blueprints ##

from rutas.main import main

app.register_blueprint(main)

from rutas.mails import mail

app.register_blueprint(mail)

## file upload ##

upload_folder = '/home/jhon/Documentos/webs/pythonProjects/masiveMailer/templates/email_templates/' 
app.config['UPLOAD_FOLDER'] = upload_folder
app.add_url_rule(
    "/uploads/<name>", endpoint="uploads", build_only=True
)

## tempdir path ##

directorio_temporal = '/home/jhon/Documentos/webs/pythonProjects/masiveMailer/uploads/tempdir/'
app.config['TEMPORARY_FOLDER'] = directorio_temporal

with app.app_context():
    db.create_all()