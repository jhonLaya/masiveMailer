from utils.db import db

# class Contactos(db.Model):
#     def __init__(self, email, nombre, create_at):
#         self.email = email 
#         self.nombre = nombre
#         self.create_at = create_at

#     id = db.Column(db.Integer(), primary_key = True)
#     email = db.Column(db.String(70), unique = True)
#     nombre = db.Column(db.String(100), unique = True)
#     create_at = db.column(db.DateTime(timezone = True))

class Email(db.Model):

    id = db.Column(db.Integer(), primary_key = True)
    asunto = db.Column(db.String(250))
    mensaje = db.Column(db.Text())
    template = db.Column(db.String(100))

    def __init__(self, asunto, mensaje, template):
        self.asunto = asunto
        self.mensaje = mensaje
        self.template = template 
