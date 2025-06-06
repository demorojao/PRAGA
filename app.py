import os
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from forms import BolsaForm, LoginForm
from extensions import db
from models import Bolsa
from flask_migrate import Migrate
from dotenv import load_dotenv
from os.path import join, exists

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicialize o Flask
app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-top')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicialização do db e Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Proteção CSRF
csrf = CSRFProtect(app)

# Função para verificar extensões permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para verificar se o usuário é admin
def is_admin():
    return session.get('user') == 'admin'

# Função para deletar a imagem
def delete_image(imagem_url):
    try:
        # Remover o arquivo da pasta de uploads
        file_path = join(app.config['UPLOAD_FOLDER'], imagem_url.split('/')[-1])
        if exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Erro ao excluir a imagem: {e}")

# Rota principal
@app.route('/')
def index():
    bolsas = Bolsa.query.all()
    return render_template('index.html', bolsas=bolsas)

# Rota de login do admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            session['user'] = 'admin'
            return redirect(url_for('index'))
        else:
            return 'Login falhou', 400
    return render_template('login.html', form=form)

# Rota de administração
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not is_admin():
        return redirect(url_for('login'))

    form = BolsaForm()
    if form.validate_on_submit():
        imagem = form.imagem.data
        if imagem and allowed_file(imagem.filename):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(imagem.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(filepath)

            nova_bolsa = Bolsa(
                nome=form.nome.data,
                descricao=form.descricao.data,
                preco=form.preco.data,
                imagem_url=f'/static/uploads/{filename}',
                whatsapp="seu-whatsapp-aqui"
            )
            db.session.add(nova_bolsa)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('admin.html', form=form)

# Rota para alternar o status de venda da bolsa (marca ou desmarca como vendida)
@app.route('/bolsa/<int:id>/alternar_vendida')
def alternar_vendida(id):
    if not is_admin():
        return redirect(url_for('login'))
    
    bolsa = Bolsa.query.get_or_404(id)
    bolsa.vendida = not bolsa.vendida  # Alterna o status de "vendida"
    db.session.commit()
    return redirect(url_for('index'))

# Marcar como vendida
@app.route('/bolsa/<int:id>/marcar_vendida')
def marcar_vendida(id):
    if not is_admin():
        return redirect(url_for('login'))
    bolsa = Bolsa.query.get_or_404(id)
    bolsa.vendida = True
    db.session.commit()
    return redirect(url_for('index'))

# Remover bolsa
@app.route('/bolsa/<int:id>/remover')
def remover_bolsa(id):
    if not is_admin():
        return redirect(url_for('login'))
    bolsa = Bolsa.query.get_or_404(id)
    
    # Remover a imagem da pasta de uploads
    delete_image(bolsa.imagem_url)
    
    db.session.delete(bolsa)
    db.session.commit()
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect(url_for('index'))

# Rodar app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
