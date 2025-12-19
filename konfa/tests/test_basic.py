
from tool.parser import parse_and_translate

def test_number():
    text = "const a = 10;"
    assert "a = 10" in parse_and_translate(text)

def test_array():
    text = "const arr = [1,2,3];"
    assert "arr = [1, 2, 3]" in parse_and_translate(text)

def test_expr():
    text = "const a = 5; const b = $a 3 +$;"
    out = parse_and_translate(text)
    assert "b = 8" in out
