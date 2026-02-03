from handlers.monitor import normalize


def test_normalize_basic_cyrillic():
    assert normalize("Привет") == "привет"
    assert normalize("ТЕСТ") == "тест"

def test_normalize_latin_translit():
    assert normalize("abc") == "авс"
    assert normalize("xep") == "хер"

def test_normalize_leet_speak():
    assert "ы" in normalize("bl")
    assert "ы" in normalize("6l")
    assert "з" in normalize("3b")

def test_normalize_mixed():
    text = "H3llo"
    expected = "нзлло"
    assert normalize(text) == expected

def test_remove_symbols():
    assert normalize("привет!!!") == "привет"
    assert normalize("тест 123") == "тестз"
