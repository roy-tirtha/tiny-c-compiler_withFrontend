"""Recursive-descent TinyC parser.
EBNF: program=statement*; statement=declaration|assignment ';'|print ';'|block|if|while|for;
expression=or; or=and ('||' and)*; and=equality ('&&' equality)*; equality=compare (('=='|'!=') compare)*;
compare=term (('<'|'>'|'<='|'>=') term)*; term=factor (('+'|'-') factor)*; factor=unary (('*'|'/'|'%') unary)*.
"""
from .ast_nodes import node
from .errors import SyntaxError_
class Parser:
 def __init__(self,tokens,source='',emit=None):self.tokens=tokens;self.i=0;self.source=source;self.emit=emit or (lambda *x:None)
 def peek(self):return self.tokens[self.i]
 def take(self,typ=None):
  t=self.peek()
  if typ and t.type!=typ:raise SyntaxError_('parser',f"Expected {typ}, found {t.type} ({t.lexeme!r})",t.line,t.column,self.source,f'Add {typ!r} or correct the preceding expression.')
  self.i+=1;return t
 def match(self,*types):
  if self.peek().type in types:return self.take()
  return None
 def parse(self):
  body=[]
  while self.peek().type!='EOF':body.append(self.statement())
  p=node('Program',body[0] if body else None,body=body);self.emit('parser.py','parse',f'Built AST with {len(body)} top-level statements',{});return p
 def statement(self):
  t=self.peek()
  if t.type=='INT':return self.declaration(True)
  if t.type=='IDENT':
   name=self.take();self.take('=');expr=self.expression();self.take(';');return node('Assign',name,name=name.lexeme,expr=expr)
  if t.type=='PRINT':
   self.take();self.take('(');expr=self.expression();self.take(')');self.take(';');return node('Print',t,expr=expr)
  if t.type=='{':return self.block()
  if t.type=='IF':
   self.take();self.take('(');cond=self.expression();self.take(')');then=self.statement();other=None
   if self.match('ELSE'):other=self.statement()
   return node('If',t,cond=cond,then=then,otherwise=other)
  if t.type=='WHILE':
   self.take();self.take('(');cond=self.expression();self.take(')');return node('While',t,cond=cond,body=self.statement())
  if t.type=='FOR':return self.for_statement()
  raise SyntaxError_('parser',f'Unexpected {t.type}',t.line,t.column,self.source,'Start a statement with int, an identifier, print, {, if, while, or for.')
 def declaration(self,semicolon):
  t=self.take('INT');name=self.take('IDENT');init=None
  if self.match('='):init=self.expression()
  if semicolon:self.take(';')
  return node('VarDecl',t,name=name.lexeme,init=init)
 def block(self):
  start=self.take('{');body=[]
  while self.peek().type not in ('}','EOF'):body.append(self.statement())
  self.take('}');return node('Block',start,body=body)
 def for_statement(self):
  t=self.take('FOR');self.take('(');init=None
  if self.peek().type!=';': init=self.declaration(False) if self.peek().type=='INT' else self.assignment_no_semicolon()
  self.take(';');cond=None if self.peek().type==';' else self.expression();self.take(';');update=None if self.peek().type==')' else self.assignment_no_semicolon();self.take(')')
  return node('For',t,init=init,cond=cond,update=update,body=self.statement())
 def assignment_no_semicolon(self):
  name=self.take('IDENT');self.take('=');return node('Assign',name,name=name.lexeme,expr=self.expression())
 def expression(self):return self.logic_or()
 def logic_or(self):return self.chain(self.logic_and,('||',))
 def logic_and(self):return self.chain(self.equality,('&&',))
 def equality(self):return self.chain(self.comparison,('==','!='))
 def comparison(self):return self.chain(self.term,('<','>','<=','>='))
 def term(self):return self.chain(self.factor,('+','-'))
 def factor(self):return self.chain(self.unary,('*','/','%'))
 def chain(self,sub,ops):
  left=sub()
  while self.peek().type in ops:
   op=self.take();left=node('BinaryOp',op,op=op.type,left=left,right=sub())
  return left
 def unary(self):
  if self.peek().type in ('-','!'):
   t=self.take();return node('UnaryOp',t,op=t.type,operand=self.unary())
  return self.primary()
 def primary(self):
  t=self.peek()
  if t.type=='NUMBER':self.take();return node('Literal',t,value=int(t.lexeme))
  if t.type=='IDENT':self.take();return node('Identifier',t,name=t.lexeme)
  if self.match('('):
   e=self.expression();self.take(')');return e
  raise SyntaxError_('parser',f'Expected expression, found {t.type}',t.line,t.column,self.source,'Use a number, declared variable, or parenthesised expression.')
