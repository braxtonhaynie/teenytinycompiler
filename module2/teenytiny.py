from lex import *
from parse import *
import sys

def main():
    print("Teeny Tiny Compiler")

    # if no file given then quit otherwise open and read 
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # init lexer and parser
    lexer =  Lexer(input)
    parser =  Parser(lexer)

    # start parser and say when done
    parser.program()
    print("Parsing completed.")


main()
