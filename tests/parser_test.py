import pytest
from ael.scanner import tokenize
from ael.parser import parse
from ael.ast import *


def test_parser_can_parse_all_the_nodes():
    source = """
       let two = 2 - 0
       print(1 * two)   // TADA 🥑 
       two = sqrt 101.3"""
    assert str(parse(tokenize(source))) == """   1 | program: Program
   2 |   statements[0]: Declaration name='two'
   3 |     initializer: BinaryExpression op='-'
   4 |       left: LiteralExpression value=2
   5 |       right: LiteralExpression value=0
   6 |   statements[1]: PrintStatement
   7 |     expression: BinaryExpression op='*'
   8 |       left: LiteralExpression value=1
   9 |       right: IdentifierExpression name='two'
  10 |   statements[2]: Assignment
  11 |     target: IdentifierExpression name='two'
  12 |     source: UnaryExpression op='sqrt'
  13 |       operand: LiteralExpression value=101.3
"""


@pytest.mark.parametrize("source, bad", [
    ("print 5 -", r"Expected id, number, unary operator, or '\('"),
    ("print 7 * ((2 _ 3)", r"Expected '\)'"),
    ("print )", r"Expected id, number, unary operator, or '\('"),
    ("x * 5", r"Expected '='"),
    ("print 5\nx * 5", r"Expected '='"),
    ("print 5\n) * 5", r"Statement expected"),
    ("let x = * 71", r"Expected id, number, unary operator, or '\('")])
def test_parser_can_detect_lots_of_errors(source, bad):
    with pytest.raises(Exception, match=bad):
        parse(tokenize(source))
