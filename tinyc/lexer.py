"""TinyC scanner with locations and trace events."""
from .tokens import Token,KEYWORDS
from .errors import LexicalError
class Lexer:
 def __init__(self,source,emit=None): self.source=source;self.i=0;self.line=1;self.column=1;self.emit=emit or (lambda *x:None)
 def advance(self):
  c=self.source[self.i];self.i+=1
  if c=='\n':self.line,self.column=self.line+1,1
  else:self.column+=1
  return c
 def scan(self):
  out=[]
  while self.i<len(self.source):
   c=self.source[self.i]
   if c.isspace():self.advance();continue
   line,col=self.line,self.column
   if self.source.startswith('//',self.i):
    while self.i<len(self.source) and self.source[self.i]!='\n':self.advance()
    continue
   if self.source.startswith('/*',self.i):
    self.advance();self.advance()
    while self.i<len(self.source) and not self.source.startswith('*/',self.i):self.advance()
    if self.i==len(self.source):raise LexicalError('lexer','Unclosed block comment',line,col,self.source,'Close it with */.')
    self.advance();self.advance();continue
   if c.isdigit():
    start=self.i
    while self.i<len(self.source) and self.source[self.i].isdigit():self.advance()
    s=self.source[start:self.i];out.append(Token('NUMBER',s,line,col));self.emit('lexer.py','scan_number',f'Read number {s}',{'line':line,'column':col});continue
   if c.isalpha() or c=='_':
    start=self.i
    while self.i<len(self.source) and (self.source[self.i].isalnum() or self.source[self.i]=='_'):self.advance()
    s=self.source[start:self.i];out.append(Token(KEYWORDS.get(s,'IDENT'),s,line,col));self.emit('lexer.py','scan_identifier',f'Read {s}',{});continue
   op=next((x for x in ('<=','>=','==','!=','&&','||') if self.source.startswith(x,self.i)),None)
   if op:self.advance();self.advance();out.append(Token(op,op,line,col));continue
   if c in '+-*/%<>=!;(),{}':self.advance();out.append(Token(c,c,line,col));continue
   raise LexicalError('lexer',f'Illegal character {c!r}',line,col,self.source,'Remove it or use a TinyC operator.')
  out.append(Token('EOF','',self.line,self.column));self.emit('lexer.py','scan',f'Finished: {len(out)-1} tokens',{});return out
def tokenize(source,emit=None):return Lexer(source,emit).scan()
