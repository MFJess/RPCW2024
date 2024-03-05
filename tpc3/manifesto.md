# TPC3 - Mapa Virtual

O objetivo do TPC3 era retirar informação de um *dataset*, no contexto de um mapa virtual, criar um grafo no GraphDB para representar as ontologias, e resolver algumas *queries* SPARQL.

## Análise do Dataset
O primeiro passo é analisar o *dataset*. Este é composto por **cidades** e **ligações**.

Data Properties da Cidade:
- Id
- Nome
- População
- Descrição
- Distrito

Data Properties da Ligação:
- Id
- Origem
- Destino
- Distância

Object Properties:
- origem (ligação -> cidade)
- destino (ligação -> cidade)

## Processamento do Dataset
O próximo passo é criar as ontologias no Protégé, assim como algumas entidades exemplo, para gerar um ficheiro facilmente alterável para se tornar um *template* para o processamento do *dataset* por inteiro.

Depois, usamos este ficheiro para criar o *script* de python, pelo qual passamos o *dataset* inteiro, para processar os dados todos e guardá-los no formato .ttl.

## GraphDB
Após ter o ficheiro .ttl, basta criar um repositório no GraphDB e importar o mesmo, de forma a poder visualizar os dados em grafos.

## Queries SPARQL
Resta-nos realizar as *queries* sobre o ficheiro importado.
Estas foram escritas e testadas no GraphDB e posteriormente guardadas no ficheiro "mapas.rq".

