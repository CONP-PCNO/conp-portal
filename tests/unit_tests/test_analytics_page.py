"""The Analytics page no longer embeds Matomo's Transitions widget."""


def test_no_transitions_widget(test_client):
    html = test_client.get('/analytics').get_data(as_text=True)
    assert 'moduleToWidgetize=Transitions' not in html
    assert 'moduleToWidgetize=UserCountryMap' in html
