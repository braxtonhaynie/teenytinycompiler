from lex import *

def main():
    input = "IF 124 foobar THEN *>/"
    lexer =  Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

    lexer.print()

main()
