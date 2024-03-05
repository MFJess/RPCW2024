# TPC2 - Escola de Música

O objetivo do TPC2 era retirar informação de um *dataset*, no contexto de uma escola de música, e criar um grafo no GraphDB para representar as ontologias.

## Análise do Dataset
O primeiro passo é analisar o *dataset*. Este é composto por **alunos**, **cursos** e **instrumentos**.

Data Properties do Aluno:
- Id
- Nome
- Data de Nascimento
- Curso
- Ano do Curso
- Instrumento

Data Properties do Curso:
- Id
- Designação
- Duração
- Instrumento

Data Properties do Instrumento:
- Id
- Texto

Object Properties:
- estuda (aluno -> curso)
- instrumentoEnsinado (curso -> instrumento)

## Processamento do Dataset
O próximo passo é criar as ontologias no Protégé, assim como algumas entidades exemplo, para gerar um ficheiro facilmente alterável para se tornar um *template* para o processamento do *dataset* por inteiro.

Depois, usamos este ficheiro para criar o *script* de python, pelo qual passamos o *dataset* inteiro, para processar os dados todos e guardá-los no formato .ttl.

## GraphDB
Após ter o ficheiro .ttl, basta criar um repositório no GraphDB e importar o mesmo, de forma a poder visualizar os dados em grafos.

