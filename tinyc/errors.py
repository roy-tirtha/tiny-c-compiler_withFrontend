"""Structured compiler diagnostics."""
class CompilerError(Exception):
    def __init__(self,stage,message,line=1,column=1,source="",hint="Review the marked source location."):
        super().__init__(message); self.stage,self.message,self.line,self.column,self.source,self.hint=stage,message,line,column,source,hint
    def to_dict(self):
        lines=self.source.splitlines()
        return {"stage":self.stage,"file":f"{self.stage}.py","message":self.message,"line":self.line,"column":self.column,"snippet":lines[self.line-1] if 0<self.line<=len(lines) else "","hint":self.hint}
class LexicalError(CompilerError): pass
class SyntaxError_(CompilerError): pass
class SemanticError(CompilerError): pass
