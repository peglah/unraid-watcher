import app.feed as feed

def test_is_stable_title():
    assert feed.is_stable_title("Unraid OS version 7.1.4 available")
    assert not feed.is_stable_title("Unraid 7.2.0-beta.1 available")

def test_latest_stable_entry():
    entries = [
        {'title': 'Unraid 7.2.0-beta.3 available', 'link': '/b', 'published': '2025-09-19T21:25:18+02:00', 'id': 'b'},
        {'title': 'Unraid OS version 7.1.4 available', 'link': '/a', 'published': '2025-06-19T01:21:00+02:00', 'id': 'a'},
    ]
    parsed = {'entries': entries}
    latest = feed.latest_stable_entry(parsed)
    assert latest['id'] == 'a'
