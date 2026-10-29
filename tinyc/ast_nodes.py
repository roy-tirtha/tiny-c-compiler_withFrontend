"""JSON serialisable AST nodes."""
from dataclasses import dataclass,field
from typing import Any
@dataclass
class Node:
    kind:str; line:int=1; column:int=1; values:dict[str,Any]=field(default_factory=dict)
    def to_dict(self):
        def c(v): return v.to_dict() if isinstance(v,Node) else [c(x) for x in v] if isinstance(v,list) else v
        return {"kind":self.kind,"line":self.line,"column":self.column,**{k:c(v) for k,v in self.values.items()}}
def node(kind,token=None,**values): return Node(kind,getattr(token,'line',1),getattr(token,'column',1),values)
