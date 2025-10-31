from app.state import State

def test_state_save_load(tmp_path):
    path = tmp_path / "state.json"
    s = State(str(path))
    s.set_last_stable("id1", "2025-10-01T00:00:00Z")
    assert s.get()['last_stable_id'] == "id1"
    s2 = State(str(path))
    assert s2.get()['last_stable_id'] == "id1"
