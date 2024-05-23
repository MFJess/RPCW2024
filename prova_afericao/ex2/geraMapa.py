import json

f = open("mapa-virtual.json")
bd = json.load(f)
f.close()

registo = """
@prefix : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32/> .

<http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#pertenceA
:pertenceA rdf:type owl:ObjectProperty ;
           owl:inverseOf :temCidade ;
           rdfs:domain :Cidade ;
           rdfs:range :Distrito .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#temCidade
:temCidade rdf:type owl:ObjectProperty ;
           rdfs:domain :Distrito ;
           rdfs:range :Cidade .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#descricaoCidade
:descricaoCidade rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#destinoLigacao
:destinoLigacao rdf:type owl:DatatypeProperty ;
                rdfs:domain :Ligacao .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#distanciaLigacao
:distanciaLigacao rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Ligacao .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#distritoCidade
:distritoCidade rdf:type owl:DatatypeProperty ;
                rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#idCidade
:idCidade rdf:type owl:DatatypeProperty ;
          rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#idLigacao
:idLigacao rdf:type owl:DatatypeProperty ;
           rdfs:domain :Ligacao .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#nomeCidade
:nomeCidade rdf:type owl:DatatypeProperty ;
            rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#origemLigacao
:origemLigacao rdf:type owl:DatatypeProperty ;
               rdfs:domain :Ligacao .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#populacaoCidade
:populacaoCidade rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Cidade .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#Cidade
:Cidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#Distrito
:Distrito rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#Ligacao
:Ligacao rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################
"""
distritos = {}

for cidade in bd['cidades']:
    cidade_retificada = cidade['nome'].replace(" ","_")
    distrito = cidade['distrito']
    if distrito in distritos.keys():
        distritos[distrito].append(cidade)
    else:
        distritos[distrito] = [cidade]

    registo += f"""
    ###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#{cidade['id']}
    :{cidade['id']} rdf:type owl:NamedIndividual ,
                            :Cidade ;
                   :pertenceA :{cidade_retificada} ;
                   :descricaoCidade "{cidade['descrição']}" ;
                   :idCidade "{cidade['id']}" ;
                   :nomeCidade "{cidade['nome']}" ;
                   :populacaoCidade "{cidade['população']}" .
    """

for ligacao in bd['ligações']:
    
    registo += f"""
    ###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#{ligacao['id']}
    :{ligacao['id']} rdf:type owl:NamedIndividual ,
                            :Ligacao ;
                    :destinoLigacao "{ligacao['destino']}" ;
                    :distanciaLigacao "{ligacao['distância']}"^^xsd:float ;
                    :origemLigacao "{ligacao['origem']}" .
    """

for distrito, cidades in distritos.items():

    distrito_retificado = distrito.replace(" ", "_")

    registo += f"""
    ###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-32#{distrito_retificado}
    :{distrito_retificado} rdf:type owl:NamedIndividual ,
                :Distrito ;
       :temCidade 
    """

    for i, cidade in enumerate(cidades):

        cidade_retificada = cidade['nome'].replace(" ", "_")

        if i == len(cidades) - 1:
            registo += f""" :{cidade_retificada}."""
        else:
            registo += f""" :{cidade_retificada},"""

print(registo)