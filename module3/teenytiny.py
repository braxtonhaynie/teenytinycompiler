from lex import *
from parse import *
from emit import *
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
    emitter = Emitter("out.c")
    parser =  Parser(lexer, emitter)

    # start parser
    parser.program()
    emitter.writeFile() # write to output file
    print("compiling done")


main()
