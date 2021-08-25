# The file contains example SPARQL queries that populate SPARQL query editor

example_query_1 = """# The query
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
    ?sub ?pred ?obj .
} LIMIT 50
"""

example_query_2 = """# The query looks for all datasets that annotated with a concept Homo sapiens
PREFIX sdo: <https://schema.org/>
SELECT DISTINCT ?datasetname ?conceptname ?uri
WHERE {
?dataset a sdo:Dataset;
    sdo:name ?datasetname;
    sdo:about ?about.  
OPTIONAL {
   ?about sdo:name ?conceptname.
}
OPTIONAL {
    { 
    ?concept sdo:identifier ?identifier_val;
        sdo:Property ?uri.
    } 
    UNION 
    { 
    ?concept sdo:value ?annotation_val;
        sdo:url ?uri.
    }

    ?conceptroot (<>|!<>) ?concept;
        sdo:name ?conceptname.
    ?about (<>|!<>)* ?conceptroot.
}
FILTER (?conceptname = "Homo sapiens"^^sdo:Text)
FILTER NOT EXISTS { ?otherdata a sdo:Dataset; sdo:hasPart ?dataset }
}
"""
