import enum
import sys

class Lexer:
    def __init__(self, input):
        # set init position and char call next char
        self.source = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    # prints out source
    def print(self):
        print()
        print(self.source, end="")

    # Processes the next char
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    # Return the next char
    def peek(self):
        return '\0' if self.curPos + 1 >= len(self.source) else self.source[self.curPos + 1]

    # Print error and exit
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # skip all white space except newline
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # skip comments
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # return next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # check what the first char
        # if multiple char operator, num, identifier, or keyword rest
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        elif self.curChar == '=':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            # used to get a string when a quote is found
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # don't allow special chars ex. \n. \r, %, etc
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character used in string.")
                self.nextChar()

            tokenText = self.source[startPos : self.curPos]
            token = Token(tokenText, TokenType.STRING)

        elif self.curChar.isdigit():
            # used when a number is encountered
            # does not support numbers like .1 or 1.
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()
            
            if self.peek() == '.':
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Illegal char in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokenText =  self.source[startPos : self.curPos  + 1]
            token = Token(tokenText, TokenType.NUMBER)

        elif self.curChar.isalpha():
            # determines if it input is a keyword or identifier
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            tokenText = self.source[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokenText)
            if keyword == None:  # identifier
                token = Token(tokenText, TokenType.IDENT)
            else: # keyword
                token = Token(tokenText, keyword)

        else:
            # unkown token
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


# contains the original text and token type
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind
    
    # used to check if token is keyword or identifier
    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
