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
     | selector
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
     | range
     
funccall : qual "(" [params] ")"
         | type "(" [params] ")"
params : expr ("," expr)*

lookup : expr "[" expr "]" 

selector : "|" "select" select_count [select_type] ["," select_attribs] "|" 
select_count : (NUM|ALL) [SORT_TYPE]
select_attribs : select_attrib ("," select_attrib)*
select_attrib : IDENT COMP_OP expr
select_type : [NEG] IDENT 

type : IDENT (_TYPESEP IDENT)* 
qual : IDENT (_VALSEP IDENT)*
range : NUM ".." [NUM]
      | [NUM] ".." NUM

_TYPESEP : "::"
_VALSEP : "."

ADD : "+"
SUB : "-"
DIV : "/"
MUL : "*"
MOD : "%"

LT : "<"
GT : ">"
LE : "<="
GE : ">="
EQ : "=="
NE : "!="
NEG : "!"

MUL_OP : MUL|DIV|MOD
ADD_OP : ADD|SUB
COMP_OP : LE|GE|EQ|NE|LT|GT

FAR : "furthest"
NEAR : "nearest"
RAND : "random"
ARB : "arbitrary"

SORT_TYPE : (FAR|NEAR|RAND|ARB)

ALL : "all"

''')

