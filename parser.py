from scanner import Scanner
from ast import *


def parse(source_code):
    the_scanner = Scanner(source_code)
    at = the_scanner.at
    match = the_scanner.match

    def parseProgram():
        statements = []
        statements.append(parseStatement())
        while at({'#IDENTIFIER', 'let', 'print'}):
            statements.append(parseStatement())
        return Program(statements)

    def parseStatement():
        if at('let'):
            return parseDeclaration()
        elif at('#IDENTIFIER'):
            return parseAssignment()
        elif at('print'):
            return parsePrintStatement()
        else:
            raise SyntaxError('Statement expected')

    def parseDeclaration():
        match('let')
        target = match('#IDENTIFIER')
        match('=')
        source = parseExpression()
        return Declaration(target, source)

    def parseAssignment():
        target = match('#IDENTIFIER')
        match("=")
        source = parseExpression()
        return Assignment(IdentifierExpression(target), source)

    def parsePrintStatement():
        match('print')
        return PrintStatement(parseExpression())

    def parseExpression():
        left = parseTerm()
        while at({"+", "-"}):
            op = match()
            right = parseTerm()
            left = BinaryExpression(op, left, right)
        return left

    def parseTerm():
        left = parseFactor()
        while at({"*", "/"}):
            op = match()
            right = parseFactor()
            left = BinaryExpression(op, left, right)
        return left

    def parseFactor():
        if at('#NUMBER'):
            return LiteralExpression(match())
        if at('#IDENTIFIER'):
            return IdentifierExpression(match())
        if at({'-', 'abs', 'sqrt'}):
            op = match()
            return UnaryExpression(op, parseExpression())
        if at('('):
            match()
            e = parseExpression()
            match(')')
            return e

    return parseProgram()