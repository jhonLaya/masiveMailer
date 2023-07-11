from flask import Blueprint, request, flash, url_for, render_template, redirect, current_app, send_from_directory
from werkzeug.utils import secure_filename
from utils.db import db
from models.contacts import Email
import os 
main = Blueprint('main', __name__)
extensiones = {'py', 'txt'}
## Contactos ##

@main.route('/')
def home():
    emails = Email.query.all()
    return render_template('main/index.html', emails = emails)

@main.route('/add_list', methods = ['GET', 'POST'])
def add_list():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Ningun archivo selecionado')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        if file and allowed_extensions(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.home'))
    return render_template('main/upload.html')

@main.route('/pruebas')
def pruebas():
    flash('pruebas de flash')
    return render_template('main/upload.html')


# @main.route('/uploads/<name>')
# def uploads(name):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)

@main.route('/email_templates/<plantillas>', methods = ['GET'])
def email_template(plantillas):
    return render_template('email_templates/' + plantillas)





## funciones ##

def allowed_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones










































# @main.route('/new_contact', methods = ['POST'])
# def new_contact():
#     pass

# @main.route('/delete/<int:id>',methods = ['POST'])
# def delete(id):
#     pass

# @main.route('/update/<int:id>', methods = ['GET', 'POST'])
# def update(id):
#     pass





