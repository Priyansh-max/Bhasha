from bhasha.text_metrics import character_error_rate, normalize_text, word_error_rate


def test_normalize_text_removes_punctuation_and_casefolds():
    assert normalize_text("Hello, WORLD!") == "hello world"


def test_word_error_rate_counts_word_substitution():
    assert word_error_rate("the weather is good", "the weather was good") == 0.25


def test_character_error_rate_counts_characters_without_spaces():
    assert round(character_error_rate("abc", "axc"), 6) == 0.333333


def test_unicode_text_normalization_keeps_arabic_and_hindi_letters():
    assert normalize_text("यह परीक्षण है।") == "यह परीक्षण है"
    assert normalize_text("هذا اختبار.") == "هذا اختبار"
