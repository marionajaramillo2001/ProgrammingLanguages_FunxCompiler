grammar funx;

// A program has 0 or more functions and 0 or 1 expression
root:
    function* codeblock EOF #RootWithExpression
    | function* EOF    #RootWithoutExpression
    ;


// A function has a name, 0 or more parameters and an associated block of code
function
        : name=FUNCNAME params=parameters '{' code=codeblock '}'
        ;

functioncall
        : name=FUNCNAME expr*
        ;

parameters
        : (VARNAME)*
        ;

codeblock
        : (statement)*
        ;

statement
        : conditional
        | while
        | expr
        | assignment
        ;

// A conditional has 1 if, 0 or more elseif and 0 or 1 else
conditional: if elseif* else? ;

if
    : IF condition=expr '{' code=codeblock '}'
    ;

elseif
    : ELSEIF condition=expr '{' code=codeblock '}'
    ;

else
    : ELSE '{' code=codeblock '}'
    ;

while
    : WHILE condition=expr '{' code=codeblock '}'
    ;

expr
    : '(' expression=expr ')'                 # Parentheses
    | TRUE                                    # True
    | FALSE                                   # False
    | functioncall                            # Call
    | <assoc=right> NOT expression=expr       # Not
    | <assoc=right> base=expr POW exp=expr    # Power
    | left=expr op=(MULT | DIV | MOD) right=expr # MultDivMod
    | left=expr op=(PLUS | MINUS) right=expr # PlusMinus
    | '-' expression=expr                     # Negative
    | left=expr op=(GT | GET | LT | LET) right=expr # Comp
    | left=expr op=(EQ | DIF ) right=expr     # EqDif
    | left=expr AND right=expr                # And
    | left=expr OR right=expr                 # Or
    | val=VALUE                               # Value
    | var=VARNAME                             # Variable
    ;

assignment
        : name=VARNAME ASSIGN expression=expr
        ;

VALUE : ('0'..'9')+ ;

// Arithmetic
MULT : '*' ;
DIV : '/' ;
PLUS : '+' ;
MINUS : '-' ;
POW : '^' ;
MOD : '%' ;



WHILE : 'while' ;

IF : 'if' ;
ELSEIF : 'elseif' ;
ELSE : 'else' ;

// Relational
EQ : '=' ;
DIF : '!=' ;
GT : '>' ;
GET : '>=' ;
LT : '<' ;
LET : '<=' ;

// Logic
NOT : 'not' ;
AND : 'and' ;
OR : 'or' ;

// Assignment
ASSIGN : '<-' ;

TRUE : 'True' ;
FALSE : 'False' ;

// Variable names start with a lowercase letter, function names start with an uppercase letter
VARNAME : ('a'..'z') ('_'|'a'..'z'|'A'..'Z'|'0'..'9')* ;
FUNCNAME : ('A'..'Z') ('_'|'a'..'z'|'A'..'Z'|'0'..'9')* ;




// Comments are skipped (~[\n] matches any character except for \n)
COMMENT : '#' (~[\n])* '\n' -> skip;

WS : [ \r\t\n]+ -> skip ;
