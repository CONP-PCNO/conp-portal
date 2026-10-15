import html
import json
import os
import re

_BLOCK_END = re.compile(r'<\s*(br\s*/?|/?\s*(p|div|li|h[1-6]|tr)(\s[^>]*)?)\s*>', re.I)
_LINK = re.compile(r'<a\s[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a\s*>', re.I | re.S)
_TAG = re.compile(r'<[^>]+>')


def _link_text(match):
    """ A link becomes its text, followed by its address when the text
        is not the address itself. """
    url, label = match.group(1).strip(), _TAG.sub('', match.group(2)).strip()
    if not label or label == url:
        return url
    return f'{label} ({url})'


def clean_description(text):
    """ Plain text for a tool description.

        Some Zenodo/Boutiques descriptions arrive as HTML, sometimes with the
        markup entity-escaped once or twice (e.g. "&lt;h1&gt;Description&lt;/h1&gt;"),
        and the card showed that markup as text. Entities are decoded (up to
        three times), line-ending tags become line breaks, other tags are
        dropped (a link keeps its text and address), and spaces are tidied. Plain-text
        descriptions are unchanged apart from whitespace.
    """
    if not isinstance(text, str):
        return text
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    text = _LINK.sub(_link_text, text)
    text = _BLOCK_END.sub('\n', text)
    text = _TAG.sub('', text)
    lines = [re.sub(r'[ \t\u00a0]+', ' ', line).strip() for line in text.split('\n')]
    text = '\n'.join(line for line in lines if line)
    return text


def get_pipelines_from_cache(search_query=None):
    cache_dir = os.path.join(os.path.expanduser(
        # @todo: remove hard-coded path and the need to read from the cache. Instead query the database for the number of pipelines.
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")

    # fetch data from cache
    with open(all_desc_path) as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path) as f:
        detailed_all_descriptors = json.load(f)

    if search_query not in ("", '', None):
        pipelines = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
            if search_query in (
                (str(descriptor.values())
                    + str(detailed_all_descriptors[d_index]["tags"].values())).lower()
                if "tags" in detailed_all_descriptors[d_index] else
                str(descriptor.values()).lower()
            )
        ]
    else:
        pipelines = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
        ]

    for pipeline in pipelines:
        for key in pipeline:
            if key.lower() == "description":
                pipeline[key] = clean_description(pipeline[key])

    return pipelines


def get_title_from_id(pipeline_id):
    pipelines = get_pipelines_from_cache()

    filtered_pipelines = list(
        filter(lambda e: e['ID'] == pipeline_id, pipelines))

    title = None
    if len(filtered_pipelines) > 0:
        pipeline = filtered_pipelines[0]
        title = pipeline.get("TITLE", None)

    return title
