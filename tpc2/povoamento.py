import json

f = open("escolamusica.json")
bd = json.load(f)
f.close()

print("""@prefix : <http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/> .

<http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#ensinadoNoCurso
:ensinadoNoCurso rdf:type owl:ObjectProperty ;
                 owl:inverseOf :instrumentoEnsinado ;
                 rdfs:domain :Instrumento ;
                 rdfs:range :Curso .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#instrumentoEnsinado
:instrumentoEnsinado rdf:type owl:ObjectProperty .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/estuda
:estuda rdf:type owl:ObjectProperty ;
        owl:inverseOf :estudadoPor ;
        rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/estudadoPor
:estudadoPor rdf:type owl:ObjectProperty ;
             rdfs:range :Aluno .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoAno
:AlunoAno rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoCurso
:AlunoCurso rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoId
:AlunoId rdf:type owl:DatatypeProperty ;
         rdfs:domain :Aluno ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoInstrumento
:AlunoInstrumento rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Aluno ;
                  rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoNascimento
:AlunoNascimento rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Aluno ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#AlunoNome
:AlunoNome rdf:type owl:DatatypeProperty ;
           rdfs:domain :Aluno ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#CursoDesignacao
:CursoDesignacao rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Curso ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#CursoDuracao
:CursoDuracao rdf:type owl:DatatypeProperty ;
              rdfs:domain :Curso ;
              rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#CursoId
:CursoId rdf:type owl:DatatypeProperty ;
         rdfs:domain :Curso ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#InstrumentoId
:InstrumentoId rdf:type owl:DatatypeProperty ;
               rdfs:domain :Instrumento ;
               rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#InstrumentoNome
:InstrumentoNome rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Instrumento ;
                 rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#Curso
:Curso rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15/Instrumento
:Instrumento rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################
""")

for aluno in bd['alunos']:
        print(f"""

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#{aluno['id']}
:{aluno['id']} rdf:type owl:NamedIndividual ,
                 :Aluno ;
        :estuda :{aluno['curso']} ;
        :AlunoAno "{aluno['anoCurso']}" ;
        :AlunoCurso "{aluno['curso']}" ;
        :AlunoId "{aluno['id']}" ;
        :AlunoInstrumento "{aluno['instrumento']}" ;
        :AlunoNascimento "{aluno['dataNasc']}" ;
        :AlunoNome "{aluno['nome']}" .
""")

for curso in bd['cursos']:
        print(f"""

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#{curso['id']}
:{curso['id']} rdf:type owl:NamedIndividual ,
              :Curso ;
     :instrumentoEnsinado :{curso['instrumento']['id']} ;
     :CursoDesignacao "{curso['designacao']}" ;
     :CursoDuracao "{curso['duracao']}" ;
     :CursoId "{curso['id']}" .
""")
        

for instrumento in bd['instrumentos']:
    print(f"""

###  http://rpcw.di.uminho.pt/2024/1/untitled-ontology-15#{instrumento['id']}
:{instrumento['id']} rdf:type owl:NamedIndividual ,
             :Instrumento ;
    :InstrumentoId "{instrumento['id']}" ;
    :InstrumentoNome "{instrumento['#text']}" .

""")

print("###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi")
