"""Build app/static/datasets/dats-field-definitions.json from
conp-documentation's CONP_DATS_fields.md (the field guide's table).

Usage (from the conp-portal root):
    python3 bin/build_dats_field_definitions.py path/to/conp-documentation/CONP_DATS_fields.md \
        app/static/datasets/dats-field-definitions.json
"""
import json
import re
import sys

src, out_path = sys.argv[1], sys.argv[2]

rows = []
for line in open(src, encoding='utf-8'):
    if line.startswith('|') and not line.startswith('|-') and 'DATS schema field' not in line:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 3:
            rows.append(cells)

# Guide paths -> the keys the Portal record uses (None: not shown separately).
KEYMAP = {'distributions.format': 'distributions.formats', 'distributions.unit': None,
          'creators.orcid': None, 'extraProperties.origin': None,
          'REB_statement': 'extraProperties.REB_statement', 'REB_number': 'extraProperties.REB_number'}

# Sentences addressed to contributors, not readers.
INSTRUCTION = re.compile(r'^(Please|We suggest|We recommend|If you provide|If you have|You must|You can|'
                         r'Note:|It must|Use the|An automatic|To be hidden|Default value|Ideally)', re.I)


def clean(t):
    t = re.sub(r'<!--.*?-->', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = t.replace('**', '').replace('_', ' ').replace('*', '')
    return re.sub(r'\s+', ' ', t).strip()


def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"“(])', t) if s.strip()]


def reader_text(t):
    kept = [s for s in sentences(t) if not INSTRUCTION.match(s)] or sentences(t)[:1]
    out = ' '.join(kept[:2])
    out = re.sub(r'^Provide (the )?', 'The ', out)
    out = re.sub(r'\byour (dataset|resource)\b', r'the \1', out)
    return out[0].upper() + out[1:] if out else out


defs = {}
for r in rows:
    path = '.'.join(p.strip() for p in r[1].split(' - '))
    m = re.match(r'extraProperties\.origin\.(\w+)$', path)
    if m:
        path = 'extraProperties.origin_' + m.group(1)
    path = KEYMAP.get(path, path)
    if not path:
        continue
    status = r[2]
    conditional = re.match(r'^\s*\*\*(REQUIRED|RECOMMENDED|OPTIONAL) IF\*\*', status) is not None
    status = re.sub(r'\*\*REQUIRED\*\* for datasets, \*\*RECOMMENDED\*\* for experiments\.\s*', '', status)
    status = re.sub(r'^\s*\*\*(REQUIRED|RECOMMENDED|OPTIONAL)( IF)?\*\*\s*', '', status)
    text = clean(r[3]) if (conditional or not clean(status)) and len(r) > 3 else clean(status)
    defs[path] = reader_text(text)

# Where the guide's wording is about filling the field in, or too long for a
# tooltip: shortened from the guide's own help text (same terms and values).
EDITED = {
    'privacy': 'The privacy level of the dataset: open (shared with the public), registered (for users who create an account or request access), controlled (after an application and approval) or private (only researchers involved in the project).',
    'distributions.access.authorizations': 'Types of verification that accessing the resource is allowed: public (available to anyone), registered (available to users authorized by the creator) or private (available only to the creator).',
    'extraProperties.CONP_status': '"CONP" = created using funding from the CONP; "Canadian" = created in Canada without CONP funding; "external" = created outside of Canada.',
    'extraProperties.REB_statement': 'The ethics permissions for the dataset.',
    'distributions.formats': 'The technical format of the dataset distribution (for example csv, nifti, txt, fasta).',
    'distributions.size': 'Total size of the dataset.',
    'licenses': 'The license(s) under which the dataset can be used.',
    'extraProperties.logo': 'The logo displayed on the resource landing page.',
    'extraProperties.derivedFrom': 'The source dataset this dataset was derived from.',
}
defs.update(EDITED)

# Groupings the guide doesn't list as fields of their own, and fields written
# by the crawlers.
ADDED = {
    'distributions': 'How the dataset is distributed: formats, size and access.',
    'distributions.access': 'Where and under what conditions the dataset can be obtained.',
    'identifier': 'A code uniquely identifying the dataset locally to a system or globally, and who minted it.',
    'primaryPublications.identifier': 'A code uniquely identifying the publication locally to a system or globally (DOI or ARK), and who minted it.',
    'alternateIdentifiers': 'Other identifiers for the same dataset.',
    'storedIn': 'The repository or data store holding the dataset.',
    'creators.roles': 'The role the creator played.',
    'creators.affiliations': 'The organizations the creator belongs to.',
    'extraProperties.downloadOptions': 'How the files are obtained; "offsite" means only from the data provider\'s own site.',
    'extraProperties.evidence_publication': 'The NeuroLibre/Evidence publication built on this dataset.',
    'extraProperties.Total number of sessions': 'The number of recording or scanning sessions in the dataset.',
    'extraProperties.source': 'The repository the CONP crawler imported this dataset from.',
    'extraProperties.osf_node_id': 'The OSF project this dataset was imported from.',
    'extraProperties.zenodo_record_id': 'The Zenodo record this dataset was imported from.',
}
for k, v in ADDED.items():
    defs.setdefault(k, v)

out = {
    '_about': ('Definitions shown as tooltips in the dataset page\'s full DATS record, keyed by DATS path '
               '(extraProperties by category). Source: CONP-PCNO/conp-documentation CONP_DATS_fields.md, '
               '"Status and Short Description" column (the help text where that column only gives a condition), '
               'without the REQUIRED/RECOMMENDED markers and sentences addressed to contributors. '
               'Shortened from the guide\'s help text: ' + ', '.join(sorted(EDITED)) + '. '
               'Not in the guide: ' + ', '.join(sorted(ADDED)) + '. '
               'To change a definition, change the field guide first, then run bin/build_dats_field_definitions.py.'),
    'fields': dict(sorted(defs.items())),
}
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write('\n')
for k, v in sorted(defs.items()):
    print(f'{k}: {v}')
