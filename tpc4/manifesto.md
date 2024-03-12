# TPC4 - Tabela Periódica

O objetivo do TPC4 era criar um *website* para expor os dados contidos num repositório do GraphDB, referente a uma tabela periódica.

Foi criada uma `app.py` criada com `flask`, que fica disponível em `localhost:5000`.

Esta app consiste nas seguintes rotas:
- `/index` -> página principal onde poderão navegar para os grupos ou elementos.
- `/elementos` -> página onde são listados todos os elementos que existem, ordenados por número atómico. Nesta página é possível navegar para a página de cada elemento clicando no respetivo nome, e para a página de cada grupo clicando no seu respetivo nome, também.
- `/elementos/id_elemento` -> página onde são apresentadas as propriedades de um determinado elemento.
- `/grupos` -> página onde são listados todos o grupos, sendo possível navegar para cada um deles clicando no grupo pretendido.
- `/grupos/id_grupo` -> página onde é apresentado um grupo, incluindo a lista de elementos que lhe pertencem, bem como todas as suas propriedades. Também é possível clicar no nome de cada elemento para navegar para a sua página.
- `/empty`-> página para onde o utilizador é redirecionado em caso de erro.

**Notas**:
- O id_elemento corresponde ao número atómico do elemento em questão.
- O id_grupo corresponde ao sufixo do grupo que vem após de `"grupo_`

