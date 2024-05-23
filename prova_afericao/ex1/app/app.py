from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

graphdb_endpoint = "http://localhost:7200/repositories/Alunos"

@app.route('/index')
def index():
    return jsonify({"data": data_iso_formatada})

# lista dos alunos, ordenada alfabeticamente por nome, com os campos: idAluno, nome e curso
@app.route('/alunos')
def alunos():
    if request.args.get('groupBy') == 'curso':
        return nrAlunosCurso()
    
    elif request.args.get('groupBy') == 'projeto':
        return projetosNotas()
    
    elif request.args.get('groupBy') == 'recurso':
        return alunosRecurso()
    
    elif 'curso' in request.args:
        return alunosCurso(request.args.get('curso'))
    
    sparql_query = """
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
        PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?id ?nome ?curso
        WHERE {
            ?aluno a :Aluno ;
                tp:idAluno ?id;
                tp:nomeAluno ?nome;
                tp:curso ?curso .
        }
        ORDER BY ?nome
    """

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"alunos": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# a informação completa de um aluno (nesta rota, considere para id o campo idAluno)
@app.route('/alunos/<id>')
def aluno(id):
    sparql_query = f"""
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
        PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?id ?nome ?curso (SUM(?tpcs) AS ?notaTotalTPCs) ?projeto ?notaExameNormal ?notaExameRecurso ?notaExameEspecial
        WHERE {{
            ?aluno :idAluno "{id}" .
            ?aluno :nomeAluno ?nome .
            ?aluno :curso ?curso .
            ?aluno :projetoNota ?projeto .
            ?aluno :fazTPC/:notaTPC ?tpcs .
            
            OPTIONAL {{
                    ?aluno :fazExame ?exameNormal .
                    ?exameNormal a tp:ExameNormal ;
                            tp:exameNota ?notaExameNormal .
            }}
            OPTIONAL {{
                        ?aluno :fazExame ?exameRecurso .
                        ?exameRecurso a tp:ExameRecurso ;
                                tp:exameNota ?notaExameRecurso .
            }}
            OPTIONAL {{
                        ?aluno :fazExame ?exameEspecial .
                        ?exameEspecial a tp:ExameEspecial ;
                                tp:exameNota ?notaExameEspecial .
            }}
        }}
        GROUP BY ?aluno ?id ?nome ?curso ?projeto ?notaExameNormal ?notaExameRecurso ?notaExameEspecial
        ORDER BY ?nome
    """

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"aluno": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# uma lista, ordenada alfabeticamente por nome, com os alunos do curso X
def alunosCurso(X):
    sparql_query = f"""
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
        PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?nomes
        WHERE {{
            ?aluno tp:curso "{X}" ;
            	tp:nomeAluno ?nomes .
        }}
    """

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"alunosCurso": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# a lista de alunos (com idAluno, nome e curso), ordenada alfabeticamente por nome, e um quarto campo correspondente ao número de TPC realizados
@app.route('/alunos/tpc')
def alunosTPC():
    sparql_query = f"""
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
            PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

            SELECT ?idAluno ?nomeAluno ?curso (COUNT(?tpc) AS ?nrTPCs)
            WHERE {{
                ?aluno a :Aluno ;
                    tp:idAluno ?idAluno ;
                    tp:nomeAluno ?nomeAluno ;
                    tp:curso ?curso ;
                    tp:fazTPC ?tpc .
                ?tpc tp:notaTPC ?nota .
                FILTER (?nota != 0.00)
            }}
            GROUP BY ?idAluno ?nomeAluno ?curso
            ORDER BY ?nomeAluno
        """

    resposta = requests.get(graphdb_endpoint,
                        params={"query": sparql_query},
                        headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"alunosTPC": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# lista de cursos, ordenada alfabeticamente, e para cada um indica quantos alunos estão registados
def nrAlunosCurso():
    sparql_query = f"""
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
        PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?curso (COUNT(?aluno) AS ?nrAlunos)
        WHERE {{
            ?aluno a :Aluno ;
                   tp:curso ?curso .
        }}
        GROUP BY ?curso
        ORDER BY ?curso
    """

    resposta = requests.get(graphdb_endpoint,
                        params={"query": sparql_query},
                        headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"nrAlunosCurso": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# uma lista de notas registadas no projeto e para cada um indica o total de alunos que a obtiveram
def projetosNotas():
    sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?nota (COUNT(?aluno) AS ?NrAlunos)
        WHERE {{
            ?aluno a tp:Aluno ;
                tp:projetoNota ?nota .
        }}
        GROUP BY ?nota
        ORDER BY ?nota
    """

    resposta = requests.get(graphdb_endpoint,
                        params={"query": sparql_query},
                        headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"projetosNotas": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})

# a lista de alunos, ordenada alfabeticamente por nome, que realizaram o exame de recurso: idAluno, nome, curso, recurso
def alunosRecurso():
    sparql_query = f"""
        PREFIX tp: <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>
        PREFIX : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/>

        SELECT ?idAluno ?nomeAluno ?curso ?recurso
        WHERE {{
            ?aluno a :Aluno ;
                   tp:idAluno ?idAluno ;
                   tp:nomeAluno ?nomeAluno ;
                   tp:curso ?curso .
            ?aluno :fazExame ?exame .
            ?exame a tp:ExameRecurso ;
                   tp:exameNota ?recurso .
        }}
        ORDER BY ?nomeAluno
    """

    resposta = requests.get(graphdb_endpoint,
                        params={"query": sparql_query},
                        headers={'Accept': 'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return jsonify({"alunosRecurso": dados, "date": data_iso_formatada})
    else:
        return jsonify({"data": data_iso_formatada})


# uma lista de alunos, ordenada alfabeticamente por nome, com o resultado final: 
# idAluno, nome, curso e notaFinal
    # em que notaFinal poderá ser "R" ou um valor entre 10 e 20 calculado da seguinte forma:
    # Se a nota do Projeto for inferior a 10 o resultado é "R";
    # Se o máximo das notas obtidas em exame for inferior a 10 o resultado é "R";
# A nota final é calculada somando todos os resultados obtidos nos TPC, e somando a
# este resultado 40% da nota do projeto e 40% da nota máxima obtida em exame; se esta
# nota final for inferior a 10 o resultado é "R" caso contrário o resultado é a nota calculada.
@app.route('/alunos/avaliados')
def alunosAvaliados():
    return jsonify({"data": data_iso_formatada})




if __name__ == '__main__': 
    app.run(debug=True, port=5001)

