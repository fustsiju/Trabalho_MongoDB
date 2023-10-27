from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.hiranzin_brabodemais
collection = db.jogos

@app.route('/')
def index():
    jogos = collection.find()
    return render_template('index.html', jogos=jogos)


@app.route('/add_product', methods=['POST'])
def add_product():
    product = {
        'nome': request.form['nome'],
        'descricao': request.form['descricao'],
        'preco': request.form['preco']
    }
    collection.insert_one(product)
    return redirect(url_for('index'))

@app.route('/delete_product/<string:product_id>', methods=['POST'])
def delete_product(product_id):
    # Convertemos o product_id para ObjectId (formato BSON)
    product_id = ObjectId(product_id)
    # Procuramos o documento com o ID especificado e o excluímos
    collection.delete_one({'_id': product_id})
    return redirect(url_for('index'))

app.run(debug=True)