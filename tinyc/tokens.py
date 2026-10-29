"""Tokens shared by the lexer and parser."""
from dataclasses import dataclass
KEYWORDS = {"int":"INT","if":"IF","else":"ELSE","while":"WHILE","for":"FOR","print":"PRINT"}
@dataclass(frozen=True)
class Token:
    type: str; lexeme: str; line: int; column: int
    def to_dict(self): return {"type":self.type,"lexeme":self.lexeme,"line":self.line,"column":self.column}
