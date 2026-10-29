# TinyC file guide

`Source -> lexer.py -> parser.py -> symbol_table.py -> semantic.py -> codegen.py -> Output`

Grammar: `program = statement*`; `statement = declaration | assignment ';' | print ';' | block | if | while | for`; expressions use `||, &&, == !=, < > <= >=, + -, * / %, unary` precedence.

| File | Purpose | Input → output |
|---|---|---|
| tokens.py | Token data | characters → tokens |
| lexer.py | Scan source | source → token list |
| ast_nodes.py | AST values | parsed structure → JSON |
| parser.py | Recursive descent | tokens → AST |
| symbol_table.py | Nested names | declarations → scoped symbols |
| semantic.py | Meaning checks | AST → findings |
| codegen.py | TAC and execution | AST → TAC/output |
| main.py | CLI/pipeline | source → result JSON |
| server.py | Offline app | HTTP → files/API |

Run: `cd tiny-c-compiler`; `python3 -m unittest discover tests`; `python3 -m tinyc.main examples/basic.tc`; `python3 -m tinyc.main --serve`.
