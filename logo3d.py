import sys

from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import EvalVisitor


def main(argv):
    input_stream = FileStream(argv[1])

    lexer = logo3dLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = logo3dParser(token_stream)
    tree = parser.root()

    visitor = EvalVisitor()
    visitor.visit(tree)
    if len(argv) == 2:
        visitor.execute_function()
    else:
        visitor.execute_function(argv[2], argv[3:])


if __name__ == "__main__":
    main(sys.argv)
