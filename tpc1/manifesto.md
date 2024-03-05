# TPC1 - Plantas

O objetivo do TPC1 era retirar informação de um *dataset*, no contexto de plantas e criar ontologias no Protégé.

## Análise do Dataset
O primeiro passo é analisar o *dataset*. Este é composto por **plantas**.

Data Properties da Planta:
- Id
- Número de Registo
- Código de rua
- Rua
- Local
- Freguesia
- Espécie
- Nome Científico
- Origem 
- Data de Plantação
- Estado
- Caldeira
- Tutor
- Implantação
- Gestor
- Data de actualização
- Número de intervenções

## Processamento do Dataset
Após perceber que a única entidade que existe é a Planta, e tudo são data properties (atributos), é só criar as ontologias no Protégé, assim como algumas entidades exemplo.
A partir destas entidades exemplos conseguimos gerar um ficheiro facilmente alterável para se tornar um *template* para o processamento do *dataset* por inteiro.

Depois, usamos este ficheiro para criar o *script* de python, pelo qual passamos o *dataset* inteiro, para processar os dados todos e guardá-los no formato .ttl.
E agora temos todos os dados processados.
