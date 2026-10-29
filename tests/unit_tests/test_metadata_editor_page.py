"""The Metadata Editor page (/dats-editor): name and Portal stylesheet."""


def test_metadata_editor_page(test_client):
    html = test_client.get('/dats-editor').get_data(as_text=True)
    assert '<h2>Metadata Editor</h2>' in html and 'CONP Portal | Metadata Editor' in html
    assert 'css/metadata-editor.css' in html
    assert 'DATS Editor' not in html
