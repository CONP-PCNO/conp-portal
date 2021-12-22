# The file contains example SPARQL queries that populate SPARQL query editor

example_query_1 = """# The query searches for all datasets that are licensed under the CC BY-NC-SA license.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
PREFIX nexus: <https://bluebrain.github.io/nexus/vocabulary/>

SELECT DISTINCT ?title ?license_name ?data_portal WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  nexus:deprecated false;
  conp:conp_portal_website ?data_portal;
  sdo:license ?license.
?license sdo:name ?license_name.
FILTER (?license_name = "CC BY-NC-SA"^^sdo:Text)
}
"""

example_query_2 = """# The query searches for all datasets that are about Alzheimer's disease.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
PREFIX nexus: <https://bluebrain.github.io/nexus/vocabulary/>

SELECT DISTINCT ?data_portal ?title ?about_name WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  nexus:deprecated false;
  conp:conp_portal_website ?data_portal;
  sdo:about ?about.
?about sdo:name ?about_name.         
FILTER regex(lcase(str(?about_name)), "alzheimer", "i")
}
"""

example_query_3 = """# The query searches for all datasets that have distribution in the MINC file format.

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
PREFIX nexus: <https://bluebrain.github.io/nexus/vocabulary/>

SELECT DISTINCT ?data_portal ?title ?format WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  nexus:deprecated false;
  conp:conp_portal_website ?data_portal;
  sdo:distribution ?distribution.
?distribution sdo:encodingFormat ?format.
FILTER (regex(str(?format), "MINC", "i"))
}
"""

example_query_4 = """# The query searches for datasets that have an authorization type set to "Public".

PREFIX sdo: <https://schema.org/>
PREFIX conp: <https://reservoir.global/v1/vocabs/Public/CONP/>
PREFIX nexus: <https://bluebrain.github.io/nexus/vocabulary/>

SELECT DISTINCT ?data_portal ?dataset_name ?value WHERE {
?dataset a sdo:Dataset;
  sdo:name ?dataset_name;
  nexus:deprecated false;
  conp:conp_portal_website ?data_portal;
  sdo:distribution ?distribution.
?distribution sdo:accessMode ?access_mode.
?access_mode sdo:permissionType ?authorization.
?authorization sdo:value ?value.
FILTER regex(lcase(str(?value)), "public", "i")
}
"""

example_query_5 = """# The query returns a list of cited papers (including their doi) with datasets that cited them.

PREFIX sdo: <https://schema.org/>
PREFIX nexus: <https://bluebrain.github.io/nexus/vocabulary/>

SELECT DISTINCT ?citation_name ?doi
(GROUP_CONCAT(DISTINCT ?title; separator=" | ") as ?datasets) 
(COUNT(DISTINCT ?title) as ?citation_count) WHERE {
?dataset a sdo:Dataset;
  sdo:name ?title;
  nexus:deprecated false;
  sdo:citation ?citation.
?citation sdo:identifier ?value;
          sdo:name ?citation_name.
?value sdo:identifier ?doi.
}
GROUP BY ?citation_name ?doi
"""
