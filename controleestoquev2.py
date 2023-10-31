from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Item {self.id}>'

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/cadastro')
def cadastro():
    items = Item.query.all()
    return render_template('cadastro.html', items=items)

@app.route('/alterar')
def alterar():
    items = Item.query.all()
    return render_template('alterar.html', items=items)

@app.route('/excluir')
def excluir():
    items = Item.query.all()
    return render_template('excluir.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    codigo = request.form['codigo']
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    item = Item(codigo=codigo, nome=nome, quantidade=quantidade)
    db.session.add(item)
    db.session.commit()
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    item_id = request.form['item_id']
    nova_quantidade = request.form['nova_quantidade']
    item = Item.query.get(item_id)
    if item:
        item.quantidade = nova_quantidade
        db.session.commit()
    return redirect('/')

@app.route('/retirar', methods=['POST'])
def retirar():
    item_id = request.form['item_id']
    quantidade_retirada = request.form['quantidade_retirada']
    item = Item.query.get(item_id)
    if item:
        item.quantidade -= int(quantidade_retirada)
        db.session.commit()
    return redirect('/')

@app.route('/devolver', methods=['POST'])
def devolver():
    item_id = request.form['item_id']
    quantidade_devolvida = request.form['quantidade_devolvida']
    item = Item.query.get(item_id)
    if item:
        item.quantidade += int(quantidade_devolvida)
        db.session.commit()
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    item_id = request.form['item_id']
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect('/')

@app.route('/pesquisa', methods=['GET', 'POST'])
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
