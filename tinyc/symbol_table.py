"""Scope stack that records every compiler interaction."""
class SymbolTable:
 def __init__(self,emit=None):self.scopes=[{}];self.operations=[];self.emit=emit or (lambda *x:None)
 def record(self,op,**data):self.operations.append({'op':op,'depth':len(self.scopes),**data});self.emit('symbol_table.py',op,op.replace('_',' '),data)
 def push(self):self.scopes.append({});self.record('push_scope')
 def pop(self):self.record('pop_scope');return self.scopes.pop()
 def declare(self,name,line):
  ok=name not in self.scopes[-1];self.record('declare',name=name,ok=ok,line=line)
  if ok:self.scopes[-1][name]={'initialized':False,'line':line,'type':'int'}
  return ok
 def lookup(self,name):
  for scope in reversed(self.scopes):
   if name in scope:self.record('lookup',name=name,ok=True);return scope[name]
  self.record('lookup',name=name,ok=False);return None
