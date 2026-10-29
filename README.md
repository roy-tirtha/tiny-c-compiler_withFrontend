# Tiny C Mini Compiler

TinyC is an offline teaching compiler and visual compiler workbench. It lexes, parses, checks scopes and initialization, lowers programs to three-address code, and executes the teaching subset.

Quick start: `cd tiny-c-compiler`; `python3 -m tinyc.main examples/basic.tc`; pipe a program with `printf 'print(2+3*4);' | python3 -m tinyc.main`; launch the studio with `python3 -m tinyc.main --serve`; run checks with `python3 -m unittest discover tests`.

The web studio shows the source editor, compiler timeline, token/AST/symbol/semantic/TAC/output details, examples, structured errors, and a clickable file guide. See `docs/tiny_c_compiler_file_guide.md` for grammar and file connections.
