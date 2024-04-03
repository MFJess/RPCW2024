from flask import Flask, render_template, url_for
from datetime import datetime
import requests
import queries

app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

# GraphDB endpoint
graphdb_endpoint = "http://epl.di.uminho.pt:7200/repositories/cinema2024"


@app.route('/')
def index():
    sparql_query = queries.quantos_filmes
    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template("index.html",data={
            "quantos":dados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

@app.route('/filmes')
def filmes():
    sparql_query = queries.filmes
    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template("filmes.html",data={
            "filmes":dados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

@app.route('/generos')
def generos():
    sparql_query = queries.generos
    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template("generos.html",data={
            "generos":dados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })
    
@app.route('/realizadores')
def realizadores():
    sparql_query = queries.realizadores
    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template("realizadores.html",data={
            "realizadores":dados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

@app.route('/atores')
def atores():
    sparql_query = queries.atores
    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template("atores.html",data={
            "atores":dados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

if __name__ == '__main__': 
    app.run(debug=True)
