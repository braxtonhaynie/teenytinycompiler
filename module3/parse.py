import sys
from lex import *
from colors import *

# Keeps track of current token  and checks if code has correct syntax
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        # keeps track of variables, labels, gotos declared
        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()

        # init tokens
        self.curToken = self.lexer.getToken()
        self.peekToken = self.lexer.getToken()

    # return true if cur token matches
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # return true if next token matches
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # find match for cur token and advance, if not error
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    # move to next token
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit(colors.FAIL + "Error: " + colors.ENDC + message)

    # Production rules

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # skip newlines 
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        
        #  parse all statements in program
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # check each goto label is declared
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    # all possible statements
    def statement(self):
        # check first token to see statement type

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # just a string
                self.nextToken()
            else:
                # expression
                self.expression()
        
        # "IF" comparison "THEN" nl {statement} "ENDIF" nl        
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")

            self.nextToken()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()

            # get statements in if
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)

        # "WHILE" comparison  "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")

            self.nextToken()
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()

            # get statements in while
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
        
        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")

            self.nextToken()

            # make sure label doesn't exist
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            
            self.nextToken()

            # keep track of goto labels
            self.labelsGotoed.add(self.curToken.text)
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            
            self.nextToken()

            # add var to table
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            
            self.nextToken()

            # add to symbol set
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)

        # unknown statement
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # newline
        self.nl()

    # nl :: = '\n' +
    def nl(self):
        print("NEWLINE")

        # at least 1 newline
        self.match(TokenType.NEWLINE)
        # loop makes sure no extra
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # check that there is a comparison operator
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator got: " + self.curToken.text)

        # keep going through expressions
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # keep getting terms
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")
        
        self.unary()
        # keep getting unary
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY", end="")

        # optional
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            print(" (" + self.curToken.text + ")")
            self.nextToken()
        else:
            print()
        self.primary()
        

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # make sure var exists
            if self.curToken.text not in self.symbols:
                self.abort("Reference variable before assignment: " + self.curToken.text)
            self.nextToken()
        else:
            # Error
            self.abort("Unexpected token at " + self.curToken.text)


    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) \
        or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) \
        or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
