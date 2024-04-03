import requests
import json

sparql_endpoint = "http://dbpedia.org/sparql"

sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?movie ?title ?actor ?director ?writer ?music
WHERE {{
  ?movie a dbo:Film ;
        rdfs:label ?title .
  OPTIONAL {{ 
    ?movie dbo:starring ?actorRaw .
    ?actorRaw rdfs:label ?actor .
  }}
  OPTIONAL {{ 
    ?film dbo:director ?directorRaw .
    ?directorRaw rdfs:label ?director .
  }}
  OPTIONAL {{ 
    ?film dbo:writer ?writerRaw .
    ?writerRaw rdfs:label ?writer .
  }}
  OPTIONAL {{ 
    ?film dbo:musicComposer ?musicRaw .
    ?musicRaw rdfs:label ?music .
  }}
  FILTER (lang(?title) = "en")
}}
LIMIT {}
OFFSET {}
"""

headers = {
    "Accept": "application/sparql-results+json"
}

limit = 1000
offset = 0
all_results = []

while True:
    query = sparql_query.format(limit, offset)

    params = {
        "query": query,
        "format": "json"
    }

    response = requests.get(sparql_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        results = response.json()
        if not results["results"]["bindings"]:
            break  
        all_results.extend(results["results"]["bindings"])
        offset += limit
    elif response.status_code == 206:
        continue
    else:
        print("Error:", response.status_code)
        print(response.text)
        break

response = requests.get(sparql_endpoint, params=params, headers=headers)


movies = {}
for result in results["results"]["bindings"]:
    movie = result["movie"]["value"]
    title = result["title"]["value"]
    actor = result.get("actor", {}).get("value", None)
    director = result.get("director", {}).get("value", None)
    writer = result.get("writer", {}).get("value", None)
    music = result.get("music", {}).get("value", None)

    if movie in movies:
        if actor and actor not in movies[movie]["actors"]:
            movies[movie]["actors"].append(actor)
        if director and director not in movies[movie]["directors"]:
            movies[movie]["directors"].append(director)
        if writer and writer not in movies[movie]["writers"]:
            movies[movie]["writers"].append(writer)
        if music and music not in movies[movie]["musicians"]:
            movies[movie]["musics"].append(music)
    else:
        movies[movie] = {
            "movie": movie,
            "actors": [actor] if actor else [],
            "directors": [director] if director else [],
            "writers": [writer] if writer else [],
            "musics": [music] if music else []
        }

movies_list = list(movies.values())

with open("cinema.json", "w") as f:
    json.dump(movies_list, f)

