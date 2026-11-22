from videonotes.backends.jsonutil import coerce_to_schema, extract_json

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "points": {"type": "array", "items": {"type": "string"}},
        "items": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}, "n": {"type": "integer"}}}},
        "kind": {"type": "string", "enum": ["a", "b"]},
        "ok": {"type": "boolean"},
    },
}


def test_extract_variants():
    assert extract_json('{"a": 1}') == {"a": 1}
    assert extract_json('Sure! Here it is:\n```json\n{"a": [1, 2,],}\n```\nHope that helps') == {"a": [1, 2]}
    assert extract_json('<think>hmm {"x": 0}</think> {"a": {"b": "}"}} trailing') == {"a": {"b": "}"}}
    assert extract_json('{"title": "Budget", "points": ["one", "tw') == {"title": "Budget", "points": ["one", "tw"]}
    assert extract_json('{"title": "Budget", "points":') == {"title": "Budget"} or extract_json('{"title": "Budget", "points":') is None
    assert extract_json("no json here") is None and extract_json("") is None and extract_json("[1,2]") is None


def test_coerce():
    got = coerce_to_schema({"title": 5, "points": "single", "items": [{"text": "x", "n": "3", "junk": 1}, None], "kind": "zzz", "extra": 1}, SCHEMA)
    assert got == {"title": "5", "points": ["single"], "items": [{"text": "x", "n": 3}], "kind": "a", "ok": False}
    assert coerce_to_schema(None, SCHEMA) == {"title": "", "points": [], "items": [], "kind": "a", "ok": False}
    assert coerce_to_schema({"points": ["a", "", None, " b "]}, SCHEMA)["points"] == ["a", "b"]
