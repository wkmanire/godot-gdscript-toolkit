from lark import Lark
import lark.indenter

grammar = r"""
start: (_NL | stmt)*

stmt: (simple_stmt _NL) | compound_stmt
simple_stmt: tool_stmt
| signal_stmt
| extends_stmt
| classname_stmt
| var_stmt
| const_stmt
| export_stmt
| onready_stmt
compound_stmt: class_def
| enum_def
| func_def

tool_stmt: "tool"
signal_stmt: "signal " NAME
extends_stmt: "extends " NAME
classname_stmt: "class_name " NAME
export_stmt: export_inf
| export_typed
export_inf: "export " var_assigned
export_typed: "export(" type ") " var_stmt
var_stmt: var_empty
| var_assigned
var_empty: "var " NAME
var_assigned: "var " NAME "=" expr
const_stmt: "const " NAME "=" expr
onready_stmt: "onready " var_stmt

func_def: "func " NAME "():" _NL func_body
func_body: _INDENT (func_stmt _NL)+ _DEDENT
func_stmt: pass_stmt
| var_stmt
pass_stmt: "pass"

enum_def: enum_regular
| enum_named
enum_regular: "enum" enum_body
enum_named: "enum" NAME enum_body
enum_body: "{" WS* [ (enum_entry [ "," ] WS*)* ] "}"
enum_entry: WORD                // (?)

class_def: "class " WORD ":" suite
suite: _NL _INDENT stmt+ _DEDENT

expr: WORD | NUMBER

type: WORD
_NL: /(\r?\n[\t ]*)+/

%declare _INDENT _DEDENT

%ignore WS_INLINE

%import common.WORD
%import common.NUMBER
%import common.WS
%import common.WS_INLINE
%import common.CNAME -> NAME
"""

class Indenter(lark.indenter.Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

parser = Lark(grammar, postlex=Indenter(), parser='lalr')

with open('scripts/recursive_tool.gd', 'r') as fh:
    content = fh.read()
    print(parser.parse(content).pretty())