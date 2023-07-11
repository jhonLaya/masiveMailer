from flask import Blueprint, request, redirect, flash, url_for, render_template, g, current_app
from werkzeug.utils import secure_filename
from mailer import mail as sender
from utils.db import db
from models.contacts import Email
from .main import extensiones, allowed_extensions
import os
from flask_mail import Message

# temp_path = current_app.config['TEMPORARY_FOLDER']

mail = Blueprint('mail', __name__, url_prefix = '/mail')

@mail.route('/new', methods = ['GET', 'POST'])
def new():
    templates = listar_directorios()

    if request.method == 'POST':
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']
        template_form = request.form['template'] 

        error = None 
        if not asunto:
            error = 'debes colocar el asunto' 

        if not mensaje:
            error = 'debes colocar el mensaje'


        if 'destinatarios' not in request.files:
            flash('No has seleccionado ningun archivo')
            return redirect(request.url)

        file = request.files['destinatarios']
        if not file:
            error = 'debes subir un archivo'
        if file and allowed_extensions(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['TEMPORARY_FOLDER'], filename))
            

        if os.path.isfile(current_app.config['TEMPORARY_FOLDER'] + file.filename):

            try:
                archive = open(current_app.config['TEMPORARY_FOLDER'] + file.filename, 'r')
                g.targets = []
                for lines in archive:
                    g.targets.append(lines.strip()) 
                os.remove(current_app.config['TEMPORARY_FOLDER'] + file.filename)   
                
            except:
                error = 'Error al abrir el archivo'
                flash(error)

        if error == None:
            msg = Message(asunto, sender = current_app.config.get('MAIL_USERNAME'), recipients = g.targets )
            if template_form == 'sin_template':
                msg.body = mensaje
            else:
                msg.body = render_template('email_templates/' + template_form, mensaje = mensaje)
                msg.html = render_template('email_templates/' + template_form, mensaje = mensaje)
            sender.send(msg)
            flash('mensaje enviado correctamente')


        ## insercion en la db ##
        new_mail = Email(asunto, mensaje, template_form)
        db.session.add(new_mail)
        db.session.commit()

        return redirect(url_for('main.home'))
 
    return render_template('mail/new.html', templates = templates)


@mail.route('/templates', methods = ['GET'])
def templates():
    templates = listar_directorios()
    return render_template('main/templates.html', templates = templates)

@mail.route('/templates_delete/<plantilla>')
def delete_plantilla(plantilla):
    os.remove(current_app.config['UPLOAD_FOLDER'] + plantilla)
    flash('eliminado exitosamente')
    return redirect(url_for('main.home'))

@mail.route('/delete/<int:id>')
def delete(id):
    emails = Email.query.get(id)
    db.session.delete(emails)
    db.session.commit()
    return redirect(url_for('main.home'))





# hmvk wzff tuma efjz

## funciones ##

def listar_directorios():
    contenido = os.listdir(current_app.config['UPLOAD_FOLDER'])
    templates = []
    for fichero in contenido:
        if os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], fichero)) and fichero.endswith('.html'):
            templates.append(fichero)    
    print(templates)        
    return templates