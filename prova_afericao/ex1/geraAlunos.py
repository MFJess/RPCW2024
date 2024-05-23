import json

f = open("alunos.json")
bd = json.load(f)
f.close()

registo = """@prefix : <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/> .

<http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#fazExame
:fazExame rdf:type owl:ObjectProperty ;
          rdfs:domain :Aluno ;
          rdfs:range :Exame .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#fazTPC
:fazTPC rdf:type owl:ObjectProperty ;
        rdfs:domain :Aluno ;
        rdfs:range :TPC .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#curso
:curso rdf:type owl:DatatypeProperty ;
       rdfs:domain :Aluno ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#exameNota
:exameNota rdf:type owl:DatatypeProperty ;
           rdfs:domain :Exame ;
           rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#idAluno
:idAluno rdf:type owl:DatatypeProperty ;
         rdfs:domain :Aluno ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#nomeAluno
:nomeAluno rdf:type owl:DatatypeProperty ;
           rdfs:domain :Aluno ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#notaTPC
:notaTPC rdf:type owl:DatatypeProperty ;
         rdfs:domain :TPC ;
         rdfs:range xsd:double .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#projetoNota
:projetoNota rdf:type owl:DatatypeProperty ;
             rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#tp
:tp rdf:type owl:DatatypeProperty ;
    rdfs:domain :TPC ;
    rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#Exame
:Exame rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#ExameEspecial
:ExameEspecial rdf:type owl:Class ;
               rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#ExameNormal
:ExameNormal rdf:type owl:Class ;
             rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#ExameRecurso
:ExameRecurso rdf:type owl:Class ;
              rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24#TPC
:TPC rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################
"""

for aluno in bd['alunos']:
    
    tpcs = set()
    for tpc in aluno['tpc']:
        tpc_id = aluno['idAluno'] + "_" + tpc['tp']
        tpcs.add(tpc_id)
    
        registo += f"""
    ###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/{tpc_id}
        :{tpc_id} rdf:type owl:NamedIndividual , :TPC ;
        :notaTPC "{tpc['nota']}"^^xsd:float ;
        :tp "{tpc['tp']}" .
        """

    exames = set()
    for tipo, nota in aluno["exames"].items():
        exameId = aluno["idAluno"] + "_" + tipo
        exameTipo = "Exame" + tipo[0].upper() + tipo[1:]
        exames.add(exameId)

        registo += f"""
    ###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/{exameId}
        :{exameId} rdf:type owl:NamedIndividual , :{exameTipo};
        :exameNota "{nota}"^^xsd:float .
        """

    registo += f""" 
###  http://rpcw.di.uminho.pt/2024/4/untitled-ontology-24/{aluno['idAluno']}
    :{aluno['idAluno']} rdf:type owl:NamedIndividual , :Aluno ;"""
    registo += "".join([f"    :fazTPC :{tpc};\n" for tpc in tpcs])+"".join([f"    :fazExame :{exame};\n" for exame in exames])
    registo += f"""
    :curso "{aluno['curso']}" ;
    :idAluno "{aluno['idAluno']}" ;
    :nomeAluno "{aluno['nome']}" ;
    :projetoNota "{aluno['projeto']}"^^xsd:int .
    """
print(registo)