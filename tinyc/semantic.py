"""All semantic findings are collected in one analysis pass."""
from .symbol_table import SymbolTable
class Analyzer:
 def __init__(self,emit=None):self.symbols=SymbolTable(emit);self.errors=[];self.warnings=[]
 def finding(self,kind,n,msg):getattr(self,kind+'s').append({'severity':kind,'message':msg,'line':n.line,'column':n.column})
 def expr(self,n):
  if not n:return
  if n.kind=='Identifier':
   symbol=self.symbols.lookup(n.values['name'])
   if not symbol:self.finding('error',n,'Undeclared variable '+n.values['name'])
   elif not symbol['initialized']:self.finding('warning',n,'Use before initialization: '+n.values['name'])
  if n.kind=='BinaryOp' and n.values['op'] in ('/','%') and n.values['right'].kind=='Literal' and n.values['right'].values['value']==0:self.finding('warning',n,'Division by constant zero')
  for v in n.values.values():
   if hasattr(v,'kind'):self.expr(v)
 def stmt(self,n):
  if not n:return
  v=n.values
  if n.kind=='Program':
   for x in v['body']:self.stmt(x)
  elif n.kind=='Block':
   self.symbols.push()
   for x in v['body']:self.stmt(x)
   self.symbols.pop()
  elif n.kind=='VarDecl':
   if not self.symbols.declare(v['name'],n.line):self.finding('error',n,'Redeclaration in this scope: '+v['name'])
   self.expr(v['init'])
   symbol=self.symbols.lookup(v['name'])
   if symbol and v['init'] is not None:symbol['initialized']=True
  elif n.kind=='Assign':
   self.expr(v['expr']);symbol=self.symbols.lookup(v['name'])
   if not symbol:self.finding('error',n,'Undeclared variable '+v['name'])
   else:symbol['initialized']=True
  elif n.kind=='Print':self.expr(v['expr'])
  elif n.kind in ('If','While'):
   self.expr(v['cond']);self.stmt(v['then'] if n.kind=='If' else v['body']);self.stmt(v.get('otherwise'))
  elif n.kind=='For':
   self.symbols.push();self.stmt(v['init']);self.expr(v['cond']);self.stmt(v['body']);self.stmt(v['update']);self.symbols.pop()
 def analyze(self,ast):self.stmt(ast);return self
