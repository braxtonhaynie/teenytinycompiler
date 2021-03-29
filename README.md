# teenytinycompiler

This is me going through the simple compiler [tutorial](http://web.eecs.utk.edu/~azh/blog/teenytinycompiler1.html) by Dr. Henley

Language syntax:

```program ::= {statement}
statement ::= "PRINT" (expression | string) nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
    | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
    | "LABEL" ident nl
    | "GOTO" ident nl
    | "LET" ident "=" expression nl
    | "INPUT" ident nl
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {( "-" | "+" ) term}
term ::= unary {( "/" | "*" ) unary}
unary ::= ["+" | "-"] primary
primary ::= number | ident
nl ::= '\n'+
```

NOTE: {} means zero or more, [] means zero or one, + means one or more of whatever is to 
the left, () is just for grouping, and | is logical or.
