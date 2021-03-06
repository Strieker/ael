import pytest
from ael.scanner import tokenize


def test_scanner_can_tokenize_the_simplest_source():
    source = "   0   "
    assert list(tokenize(source)) == [
        ('#NUMBER', '0'),
        ('#END', '')]


def test_scanner_can_tokenize_a_program_with_all_tokens():
    source = """   let x = 5 * 9
        x = x + (2 - 8) / 8999
        let 大きい犬 = x // look it is a comment

        // that was a blank line
        print 大きい犬 / 1.2
        """
    assert list(tokenize(source)) == [
        ('#KEYWORD', 'let'),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '='),
        ('#NUMBER', '5'),
        ('#SYMBOL', '*'),
        ('#NUMBER', '9'),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '='),
        ('#IDENTIFIER', 'x'),
        ('#SYMBOL', '+'),
        ('#SYMBOL', '('),
        ('#NUMBER', '2'),
        ('#SYMBOL', '-'),
        ('#NUMBER', '8'),
        ('#SYMBOL', ')'),
        ('#SYMBOL', '/'),
        ('#NUMBER', '8999'),
        ('#KEYWORD', 'let'),
        ('#IDENTIFIER', '大きい犬'),
        ('#SYMBOL', '='),
        ('#IDENTIFIER', 'x'),
        ('#KEYWORD', 'print'),
        ('#IDENTIFIER', '大きい犬'),
        ('#SYMBOL', '/'),
        ('#NUMBER', '1.2'),
        ('#END', '')]


def test_scanner_distinguishes_keywords_and_identifiers():
    source = "let lety le t"
    assert list(tokenize(source)) == [
        ('#KEYWORD', 'let'),
        ('#IDENTIFIER', 'lety'),
        ('#IDENTIFIER', 'le'),
        ('#IDENTIFIER', 't'),
        ('#END', '')]


def test_scanner_allows_comment_on_last_line():
    source = "2//5"
    assert list(tokenize(source)) == [
        ('#NUMBER', '2'),
        ('#END', '')]


@pytest.mark.parametrize("source, bad", [
    ("1. hello", r"."),
    ("9 )$", r"\$"),
    ("9+--2z!", r"!"),
    ("x&y", r"&")])
def test_scanner_detects_lexical_errors(source, bad):
    with pytest.raises(Exception, match=f"Unexpected character: '{bad}'"):
        list(tokenize(source))
