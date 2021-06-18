import sqlite3
from flask import Flask, g, render_template, request

# Configurações

DATABASE = './flaskr.db'
SECRET_KEY = "pudim" # Chave do BD. Em produção não é hardcoded nem simples ou curta
USERNAME = 'admin'
PASSWORD = 'admin'

# Aplicação

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before():
    g.db = connect_db()

@app.teardown_request
def after(exception):
    g.db.close()


@app.route('/') # Rota do conteúdo, a partir do domínio
def index(): # Index da página
    sql = 'SELECT titulo, texto from entradas order by id desc'
    cur = g.db.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto) for titulo, texto in cur.fetchall()]
    #entradas = [{'titulo': 'O primeiro Post',
    #            'texto': 'texto do post'},
    #            {'titulo': 'segundo post',
    #            'texto': 'segundo texto'}
    #            ]
    return render_template('index.html', entradas=entradas)

@app.route('/inserir', methods=['POST'])
def inserir():
    sql = "INSERT INTO entradas(titulo, texto) values (?, ?)"
    g.db.execute(sql, [request.form['titulo'], request.form['texto']])
    g.gb.commit()
    return render_template('index.html')