# models.py

from extensions import db

class Bolsa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    vendida = db.Column(db.Boolean, default=False)  # Campo para marcar como vendida


    def __repr__(self):
        return f'<Bolsa {self.nome}>'

from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Armazenando a senha (deve ser criptografada)
    
    def __repr__(self):
        return f'<User {self.username}>'
