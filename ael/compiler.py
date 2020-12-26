"""A commpiler for Ael

You can run this compiler from the command line, for example:

    python ael/compiler.py some/cool/file.ael output_type

or simply include this module in a larger app and invoke the compile function:

    compile(source_code_of_some_program, output_type)

to print the target program to standard output. The option tells the compiler
what to print to standard output:

    tokens     the token sequence
    ast        the abstract syntax tree
    analyzed   the semantically analyzed representation
    optimized  the optimized semantically analyzed representation
    js         the translation to JavaScript
    c          the translation to C
    llvm       the translation to LLVM
"""

from scanner import tokenize
from parser import parse
from ast import print_tree
from analyzer import analyze, print_graph
from optimizer import optimize
from generator import generate


def compile(source, output_type):
    if output_type == 'tokens':
        for token in tokenize(source):
            print(token)
    elif output_type == 'ast':
        print_tree(parse(source))
    elif output_type == 'analyzed':
        print_graph(analyze(parse(source)))
    elif output_type == 'optimized':
        print_graph(optimize(analyze(parse(source))))
    elif output_type in ('js', 'c', 'llvm'):
        print(generate[output_type](optimize(analyze(parse(source)))))
    else:
        print('Unrecognized output type')


if __name__ == '__main__':
    from sys import argv
    from pathlib import Path
    if len(argv) != 3:
        print('Syntax: python ael/compiler.py filename output_type')
    else:
        compile(Path(argv[1]).read_text(), argv[2])
