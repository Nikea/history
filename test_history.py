from historydict import HistoryDict
import pytest

OBJ_ID_LEN = 36


@pytest.fixture
def h():
    return HistoryDict(":memory:")


def test_historydict(h):
    run_id = "".join(["a"] * OBJ_ID_LEN)
    # Simple round-trip: put and past
    config1 = {"plot_x": "long", "plot_y": "island"}
    h._put(run_id, config1)
    result1 = h.past(run_id)
    assert result1 == config1

    # Put a second entry. Check that past returns most recent.
    config2 = {"plot_x": "new", "plot_y": "york"}
    h._put(run_id, config2)
    result2 = h.past(run_id)
    assert result2 == config2
    # And.past(..., 1) returns previous.
    result1 = h.past(run_id, 1)
    assert result1 == config1


def test_clear(h):
    h._put("hi", "mom")
    h.clear()
    with pytest.raises(KeyError):
        h.past("hi")


def test_trim(h):
    with pytest.raises(NotImplementedError):
        h.trim()


def test_neg_numback_fails(h):
    with pytest.raises(ValueError):
        h.past("test", -1)


def test_nonexistent_past_fails(h):
    h["cats"] = 123
    with pytest.raises(ValueError):
        h.past("cats", 1)
    h["cats"] = 456
    h.past("cats", 1)  # should not raise


def test_gs_items(h):
    h[123] = "aardvark"
    assert h[123] == "aardvark"


def test_opening(tmp_path):
    filename = tmp_path / "test"
    h1 = HistoryDict(filename)
    h1["aardvark"] = "ants"
    del h1

    h2 = HistoryDict(filename)
    assert h2["aardvark"] == "ants"


def test_iter(h):
    keys = set("abcd")
    for k in keys:
        h[k] = k
    for k, v in h.items():
        assert k == v


def test_del(h):
    h["a"] = 123
    h["a"] = 456
    assert "a" in h
    del h["a"]
    assert "a" not in h
    # Add a value back to check that all old values were cleared.
    h["a"] = 789
    with pytest.raises(ValueError):
        h.past("a", 1)
    assert h["a"] == 789
    assert h.past("a", 0) == 789


def test_no_key_in_del(h):
    with pytest.raises(KeyError):
        del h["aardvark"]


def test_len(h):
    keys = set("abcd")
    for k in keys:
        h[k] = k

    assert len(keys) == len(h)


def test_get(h):
    b = h.get("b", "aardvark")
    assert b, "aardvark"


def test_protected_key(h):
    with pytest.raises(ValueError):
        h[HistoryDict.RESERVED_KEY_KEY]
    with pytest.raises(ValueError):
        h[HistoryDict.RESERVED_KEY_KEY] = "aardvark"


def test_repr(h):
    kvpairs = (("foo", "bar"), ("spam", "spam spam spam"))
    dct = {}
    for k, v in kvpairs:
        dct[k] = v
        h[k] = v
    assert repr(dict(h)) == repr(h)
    assert dict(h) == dct


def test_flush(tmp_path):
    pth = tmp_path / "test.db"
    # Needed for windows compatibility
    g = HistoryDict(pth)
    g["k"] = {"a": 1}
    g["k"]["a"] = 2
    # Check that mutated value persists.
    del g
    g = HistoryDict(pth)
    assert g["k"]["a"] == 2

    # finally smoke test the API
    g.flush()
    g._flush("k")
