from lark import Lark

parser = Lark(r'''
%import common.WS
%import common.CNAME -> IDENT
%import common.SIGNED_INT -> NUM
%import common.ESCAPED_STRING -> STRING

COMMENT: /#[^\n]*/
%ignore COMMENT
%ignore WS

start : toplevel_clause*

toplevel_clause : namespace_clause
                | function_clause
                | import_clause
                

namespace_clause : "namespace" IDENT
function_clause : funcspec paramspec stmt
import_clause : "import" qual

paramspec : "(" (type IDENT)* ")"
attrib : IDENT ["[" atom "]"]
attribspec : attrib*
funcspec : "func" type IDENT
         | "func" "constructor" IDENT -> funcspec_constructor
         

stmt : block_stmt
     | expr_stmt
     | var_stmt

block_stmt : "{" stmt* "}"
expr_stmt : expr ";"
var_stmt : type IDENT "=" expr ";"
         | qual "=" expr ";"       -> assign_stmt

expr : "(" expr ")"
     | atom
     | lookup
     | funccall
     | mul_expr
     | add_expr
     
mul_expr : expr MUL_OP expr
add_expr : expr ADD_OP expr

atom : NUM
     | qual
     | STRING
     
funccall : qual "(" [params] ")"
         | type "(" [params] ")"
params : expr ("," expr)*

lookup : expr "[" expr "]" 

type : IDENT (_TYPESEP IDENT)* 
qual : IDENT (_VALSEP IDENT)*

_TYPESEP : "::"
_VALSEP : "."

ADD : "+"
SUB : "-"
DIV : "/"
MUL : "*"
MOD : "%"

MUL_OP : MUL|DIV|MOD
ADD_OP : ADD|SUB

''')

