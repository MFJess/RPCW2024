import json

f = open("plantas.json")
bd = json.load(f)
f.close()

print("""@prefix : <http://www.semanticweb.org/jess/ontologies/2024/1/plantas/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/jess/ontologies/2024/1/plantas/> .

<http://www.semanticweb.org/jess/ontologies/2024/1/plantas> rdf:type owl:Ontology ;
                                                             owl:versionIRI <http://www.semanticweb.org/jess/ontologies/2024/1/plantas> .

#################################################################
#    Object Properties
#################################################################

###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/contem
:contem rdf:type owl:ObjectProperty ;
        owl:inverseOf :temRua ;
        rdfs:domain :Rua ;
        rdfs:range :Planta .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/temRua
:temRua rdf:type owl:ObjectProperty ;
        rdfs:domain :Planta ;
        rdfs:range :Rua .


#################################################################
#    Data properties
#################################################################

###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Caldeira
:Caldeira rdf:type owl:DatatypeProperty ;
          rdfs:domain :Planta ;
          rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Código_de_rua
:Código_de_rua rdf:type owl:DatatypeProperty ;
               rdfs:domain :Rua ;
               rdfs:range xsd:long .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Data_de_Plantação
:Data_de_Plantação rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Data_de_actualização
:Data_de_actualização rdf:type owl:DatatypeProperty ;
                      rdfs:domain :Planta ;
                      rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Espécie
:Espécie rdf:type owl:DatatypeProperty ;
         rdfs:domain :Planta ;
         rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Estado
:Estado rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Freguesia
:Freguesia rdf:type owl:DatatypeProperty ;
           rdfs:domain :Rua ;
           rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Gestor
:Gestor rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Id
:Id rdf:type owl:DatatypeProperty ;
    rdfs:domain :Planta ;
    rdfs:range xsd:long .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Implantação
:Implantação rdf:type owl:DatatypeProperty ;
             rdfs:domain :Planta ;
             rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Local
:Local rdf:type owl:DatatypeProperty ;
       rdfs:domain :Rua ;
       rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Nome_científico
:Nome_científico rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Planta ;
                 rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Número_de_Intervenções
:Número_de_Intervenções rdf:type owl:DatatypeProperty ;
                        rdfs:domain :Planta ;
                        rdfs:range xsd:int .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Número_de_Registo
:Número_de_Registo rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:int .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Origem
:Origem rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Rua
:Rua rdf:type owl:DatatypeProperty ;
     rdfs:domain :Planta ,
                 :Rua ;
     rdfs:range xsd:string .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Tutor
:Tutor rdf:type owl:DatatypeProperty ;
       rdfs:domain :Planta ;
       rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Planta
:Planta rdf:type owl:Class .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas/Rua
:Rua rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################
""")


for planta in bd:
    registo = f"""
###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta['Código de rua']}
<http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta['Código de rua']}> rdf:type owl:NamedIndividual ,
                                                                             :Rua ;
                                                                    :contem <http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta["Id"]}> ;
                                                                    :Código_de_rua "{planta["Código de rua"]}" ;
                                                                    :Freguesia "{planta["Freguesia"]}" ;
                                                                    :Local "{planta["Local"]}" ;
                                                                    :Rua "{planta["Rua"].replace('"','')}" .


###  http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta['Id']}
<http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta['Id']}> rdf:type owl:NamedIndividual ,
                                                                              :Planta ;
                                                                     :temRua <http://www.semanticweb.org/jess/ontologies/2024/1/plantas#{planta["Código de rua"]}> ;
                                                                     :Caldeira "{planta["Caldeira"]}" ;
                                                                     :Data_de_Plantação "{planta["Data de Plantação"]}" ;
                                                                     :Data_de_actualização "{planta["Data de actualização"]}" ;
                                                                     :Espécie "{planta["Espécie"]}" ;
                                                                     :Estado "{planta["Estado"]}" ;
                                                                     :Gestor "{planta["Gestor"]}" ;
                                                                     :Implantação "{planta["Implantação"]}" ;
                                                                     :Nome_Científico "{planta["Nome Científico"]}" ;
                                                                     :Número_de_intervenções "{planta["Número de intervenções"]}" ;
                                                                     :Número_de_Registo "{planta["Número de Registo"]}" ;
                                                                     :Origem "{planta["Origem"]}" ;
                                                                     :Rua "{planta["Rua"].replace('"','')}" ;
                                                                     :Tutor "{planta["Tutor"]}" .
"""
    
    print(registo)

print("###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi")