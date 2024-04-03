quantos_filmes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://rpcw.di.uminho.pt/2024/cinema> 

SELECT (COUNT(?s) AS ?totalFilmes) WHERE {
    ?s rdf:type c:Film .
} 
"""

filmes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://rpcw.di.uminho.pt/2024/cinema> 

select * where {
    ?filme rdf:type c:Film .
    OPTIONAL {?filme c:title ?titulo }.
    OPTIONAL {?filme c:description ?descricao }.
    OPTIONAL {?filme c:duration ?duracao }.    
} 
ORDER BY ?titulo
"""

generos = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://rpcw.di.uminho.pt/2024/cinema> 

select ?genre where {
    ?a rdf:type c:Film.
	?a c:hasGenre ?genre.
}
"""

realizadores = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://rpcw.di.uminho.pt/2024/cinema> 

select * where {
    ?s rdf:type c:Director .
} 
"""

atores = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX c: <http://rpcw.di.uminho.pt/2024/cinema> 

select * where {
    ?s rdf:type c:Actor .
} 
"""
