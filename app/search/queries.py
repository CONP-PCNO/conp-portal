# The file contains example SPARQL queries that populate SPARQL query editor

example_query_1 = """# The query searches for all datasets that are licensed under the CC BY-NC-SA license.

PREFIX sdo: <https://schema.org/>
SELECT DISTINCT ?title ?license_name WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  sdo:license ?license.
  ?license sdo:name ?license_name.
FILTER (?license_name = "CC BY-NC-SA"^^sdo:Text)
}
"""

example_query_2 = """# The query searches for all datasets that are about Alzheimer's.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
SELECT DISTINCT ?dataset ?title ?about_name WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  sdo:about ?about.
?about sdo:name ?about_name.         
FILTER regex(lcase(str(?about_name)), "alzheimer", "i")
}
"""

example_query_3 = """# The query searches for all datasets that have distribution in the MINC file format.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
SELECT DISTINCT ?dataset ?title ?format WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  sdo:distribution ?distribution.
  ?distribution conp:formats ?format.
FILTER (regex(?format, "MINC", "i"))
}"""

example_query_4 = """# The query searches for datasets that have an authorization type set to "Public".

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
SELECT DISTINCT ?dataset_name ?value
WHERE {
    ?dataset a sdo:Dataset;
        sdo:name ?dataset_name;
        sdo:distribution ?distribution.
  ?distribution sdo:accessMode ?access_mode.
  ?access_mode conp:authorizations ?authorization.
  ?authorization sdo:value ?value.
FILTER regex(lcase(str(?value)), "public", "i")
}
"""

example_query_5 = """# The query returns all datasets and their content size.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
SELECT DISTINCT ?dataset_name ?content_size ?value
WHERE {
    ?dataset a sdo:Dataset;
        sdo:name ?dataset_name;
        sdo:distribution ?distribution.
  ?distribution sdo:contentSize ?content_size;
                conp:unit ?unit.
  ?unit sdo:value ?value.
}
"""
