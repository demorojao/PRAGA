from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class BolsaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    preco = DecimalField('Preço', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
