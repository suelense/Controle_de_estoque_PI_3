from flask import Flask, render_template, request, redirect, session,url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta'  # Chave secreta para manter a sessão segura
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Item {self.id}>'

# Decorador para verificar se o usuário está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_page'))  # Redireciona para a página de login se não estiver autenticado
        return f(*args, **kwargs)
    return decorated_function


# Rota para a página de login principal
@app.route('/login0', methods=['GET', 'POST'])
def login0():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar as credenciais do usuário (exemplo simplificado)
        user = Usuario.query.filter_by(usuario=username, senha=password).first()
        if user:
            session['logged_in'] = True
            return redirect('/index')
        else:
            return 'Credenciais inválidas. <a href="/login0">Tente novamente</a>'
    else:
        return render_template('login0.html')


# Rota para a página de login e cadastro de usuários INTERNA
@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']  # Verifica se é uma tentativa de login ou cadastro

        if action == 'login':
            # Verificar as credenciais do usuário (exemplo simplificado)
            user = Usuario.query.filter_by(usuario=username, senha=password).first()
            if user:
                session['logged_in'] = True
                return redirect('/index')
            else:
                return 'Credenciais inválidas. <a href="/login0">Tente novamente</a>'
        elif action == 'cadastrar':
            # Verifica se o usuário já existe no banco de dados
            if Usuario.query.filter_by(usuario=username).first():
                return 'Usuário já existe. <a href="/login">Tente novamente</a>'

            # Cria um novo usuário e adiciona ao banco de dados
            new_user = Usuario(usuario=username, senha=password)
            db.session.add(new_user)
            db.session.commit()

            return 'Usuário cadastrado com sucesso! <a href="/login">Voltar para a página de login</a>'
    else:
        return render_template('login.html')

# Rota para logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return 'Você foi desconectado com sucesso! <a href="/login0">Vá para a página de login</a>'

@app.route('/')
def login_page():
    return render_template('login0.html')


@app.route('/index')
@login_required
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/cadastro')
@login_required
def cadastro():
    items = Item.query.all()
    return render_template('cadastro.html', items=items)

@app.route('/alterar')
@login_required
def alterar():
    items = Item.query.all()
    return render_template('alterar.html', items=items)

@app.route('/excluir')
@login_required
def excluir():
    items = Item.query.all()
    return render_template('excluir.html', items=items)

@app.route('/add', methods=['POST'])
@login_required
def add():
    codigo = request.form['codigo']
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    item = Item(codigo=codigo, nome=nome, quantidade=quantidade)
    db.session.add(item)
    db.session.commit()
    return redirect('/index')

@app.route('/update', methods=['POST'])
@login_required
def update():
    item_id = request.form['item_id']
    nova_quantidade = request.form['nova_quantidade']
    item = Item.query.get(item_id)
    if item:
        item.quantidade = nova_quantidade
        db.session.commit()
    return redirect('/index')

@app.route('/retirar', methods=['POST'])
@login_required
def retirar():
    item_id = request.form['item_id']
    quantidade_retirada = request.form['quantidade_retirada']
    item = Item.query.get(item_id)
    if item:
        item.quantidade -= int(quantidade_retirada)
        db.session.commit()
    return redirect('/index')

@app.route('/devolver', methods=['POST'])
@login_required
def devolver():
    item_id = request.form['item_id']
    quantidade_devolvida = request.form['quantidade_devolvida']
    item = Item.query.get(item_id)
    if item:
        item.quantidade += int(quantidade_devolvida)
        db.session.commit()
    return redirect('/index')

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    item_id = request.form['item_id']
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/index')

@app.route('/pesquisa', methods=['GET', 'POST'])
@login_required
def pesquisa():
    item = None
    not_found = False

    if request.method == 'POST':
        codigo = request.form['codigo']
        item = Item.query.filter_by(codigo=codigo).first()
        if not item:
            not_found = True

    return render_template('pesquisa.html', item=item, not_found=not_found)

if __name__ == '__main__':
    app.run(debug=True)