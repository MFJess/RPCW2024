from flask import Flask, render_template, url_for
from datetime import datetime
import requests

app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

# GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/Tabela-Periodica"


@app.route('/')
def index():
    return render_template('index.html', data = {"data":data_iso_formatada})


def corrige_id_grupo(elemento):
    elemento['grupo']["value"] = elemento["grupo"]["value"].split("#")[1]
    return elemento

# ✨✨✨
@app.route('/elementos')
def elementos():
    sparql_query = """
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
select * where{
    ?s a tp:Element ;
        tp:name ?nome;
        tp:symbol ?simb;
        tp:atomicNumber ?n;
        tp:group ?grupo.
    ?grupo tp:name ?grupo_nome.
}
order by ?n
"""

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    print(resposta.status_code)
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        dados_tratados = map(corrige_id_grupo, dados)
        return render_template("elementos.html",data={
            "elements":dados_tratados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

##############################################

def corrige_grupo(grupo):
    grupo['grupo_id']["value"] = grupo["grupo_id"]["value"].split("#")[1]
    grupo['grupo_nome'] = grupo.get("grupo_nome", {'type': 'literal', 'value': '-'}) 
    grupo['grupo_numero'] = grupo.get("grupo_numero", {'type': 'literal', 'value': '-'})
    return grupo

@app.route('/grupos')
def grupos():
    sparql_query = """
PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?grupo_id ?grupo_numero ?grupo_nome 
WHERE {
     ?grupo_id rdf:type tp:Group .
     OPTIONAL {?grupo_id tp:name ?grupo_nome }
     OPTIONAL {?grupo_id tp:number ?grupo_numero }
}
ORDER BY ?grupo_numero
"""

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    print(resposta.status_code)
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        dados_tratados = map(corrige_grupo, dados)
        return render_template("grupos.html",data={
            "grupos":dados_tratados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

##############################################
    
def corrige_elemento(elemento):
    elemento['elemento_bloco']['value'] = (elemento['elemento_bloco']['value'].split("#")[-1]).split("-")[0]
    elemento['elemento_periodo']['value'] = elemento['elemento_periodo']['value'].split("_")[-1]
    elemento['elemento_class']['value'] = elemento['elemento_class']['value'].split("#")[-1]
    elemento['elemento_estado']['value'] = elemento['elemento_estado']['value'].split("#")[-1]
    return elemento

@app.route('/grupos/<string:id>')
def grupo(id):
    sparql_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT ?elemento_simb ?elemento_nome (STR(?elemento_na_raw) AS ?elemento_na) ?elemento_bloco (STR(?elemento_peso_raw) AS ?elemento_peso) ?elemento_periodo ?elemento_class ?elemento_estado ?elemento_cor
    WHERE {
        ?grupo_id rdf:type tp:Group .
        ?elemento tp:group ?grupo_id ;
                tp:name ?elemento_nome ;
                tp:atomicNumber ?elemento_na_raw ;
                tp:atomicWeight ?elemento_peso_raw ;
                tp:period ?elemento_periodo ;
                tp:symbol ?elemento_simb ;
                tp:classification ?elemento_class ;
                tp:block ?elemento_bloco ;
                tp:color ?elemento_cor ;
                tp:standardState ?elemento_estado .

        FILTER (?grupo_id = tp:""" + id + """)
    }
    ORDER BY ?elemento_simb 
    """

    resposta = requests.get(graphdb_endpoint, params={"query": sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        dados_tratados = map(corrige_elemento, dados)
        grupo_id = id.split("_")[-1]
        return render_template("grupo.html", data={
           "grupo":dados_tratados,
           "grupo_id":grupo_id,
           "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
           "data":data_iso_formatada
        })

#########################################################

@app.route('/elementos/<string:id>')
def elemento(id):
    sparql_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

    SELECT ?elemento_simb ?elemento_nome (STR(?elemento_na_raw) AS ?elemento_na) ?elemento_bloco (STR(?elemento_peso_raw) AS ?elemento_peso) ?elemento_periodo ?elemento_class ?elemento_estado ?elemento_cor 
    WHERE {
        ?elemento rdf:type tp:Element ;
                tp:atomicNumber ?elemento_na_raw ;
                tp:name ?elemento_nome ;
                tp:atomicWeight ?elemento_peso_raw ;
                tp:period ?elemento_periodo ;
                tp:symbol ?elemento_simb ;
                tp:classification ?elemento_class ;
                tp:block ?elemento_bloco ;
                tp:color ?elemento_cor ;
                tp:standardState ?elemento_estado .
        FILTER (?elemento_na_raw = """ + id + """)
    }
    """
    resposta = requests.get(graphdb_endpoint, params={"query": sparql_query}, headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        dados_tratados = list(map(corrige_elemento, dados))
        print(dados_tratados)
        return render_template("elemento.html", data={
            "elemento":dados_tratados,
            "date":data_iso_formatada
        })
    else:
        return render_template("empty.html",data={
            "data":data_iso_formatada
        })

if __name__ == '__main__': 
    app.run(debug=True)
