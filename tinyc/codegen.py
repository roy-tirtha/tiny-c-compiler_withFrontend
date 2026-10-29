"""Three-address code generator and deterministic TinyC interpreter."""
class Generator:
 def __init__(self,emit=None):self.lines=[];self.temp=0;self.label=0;self.emit=emit or (lambda *x:None)
 def add(self,text,node=None):self.lines.append({'text':text,'line':getattr(node,'line',1)});self.emit('codegen.py','emit',text,{'line':getattr(node,'line',1)})
 def new_temp(self):self.temp+=1;return f't{self.temp}'
 def new_label(self):self.label+=1;return f'L{self.label}'
 def expr(self,n):
  v=n.values
  if n.kind=='Literal':return str(v['value'])
  if n.kind=='Identifier':return v['name']
  if n.kind=='UnaryOp':
   t=self.new_temp();self.add(f'{t} = {v["op"]}{self.expr(v["operand"])}',n);return t
  a,b=self.expr(v['left']),self.expr(v['right']);t=self.new_temp();self.add(f'{t} = {a} {v["op"]} {b}',n);return t
 def stmt(self,n):
  if not n:return
  v=n.values
  if n.kind in ('Program','Block'):
   for x in v['body']:self.stmt(x)
  elif n.kind=='VarDecl':
   if v['init'] is not None:self.add(f'{v["name"]} = {self.expr(v["init"])}',n)
  elif n.kind=='Assign':self.add(f'{v["name"]} = {self.expr(v["expr"])}',n)
  elif n.kind=='Print':self.add(f'print {self.expr(v["expr"])}',n)
  elif n.kind=='If':
   end=self.new_label();other=self.new_label() if v['otherwise'] else end;self.add(f'ifFalse {self.expr(v["cond"])} goto {other}',n);self.stmt(v['then'])
   if v['otherwise']:self.add(f'goto {end}',n);self.add(f'{other}:',n);self.stmt(v['otherwise'])
   self.add(f'{end}:',n)
  elif n.kind=='While':
   start,end=self.new_label(),self.new_label();self.add(f'{start}:',n);self.add(f'ifFalse {self.expr(v["cond"])} goto {end}',n);self.stmt(v['body']);self.add(f'goto {start}',n);self.add(f'{end}:',n)
  elif n.kind=='For':
   self.stmt(v['init']);start,end=self.new_label(),self.new_label();self.add(f'{start}:',n)
   if v['cond'] is not None:self.add(f'ifFalse {self.expr(v["cond"])} goto {end}',n)
   self.stmt(v['body']);self.stmt(v['update']);self.add(f'goto {start}',n);self.add(f'{end}:',n)
 def generate(self,ast):self.stmt(ast);return self.lines
 def run(self,ast):
  env={};out=[]
  def ev(n):
   v=n.values
   if n.kind=='Literal':return v['value']
   if n.kind=='Identifier':return env.get(v['name'],0)
   if n.kind=='UnaryOp':return -ev(v['operand']) if v['op']=='-' else int(not ev(v['operand']))
   a,b=ev(v['left']),ev(v['right']);op=v['op']
   return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a//b,'%':lambda:a%b,'<':lambda:int(a<b),'>':lambda:int(a>b),'<>':lambda:int(a!=b),'<=':lambda:int(a<=b),'>=':lambda:int(a>=b),'==':lambda:int(a==b),'!=':lambda:int(a!=b),'&&':lambda:int(bool(a) and bool(b)),'||':lambda:int(bool(a) or bool(b))}[op]()
  def run(n):
   if not n:return
   v=n.values
   if n.kind in ('Program','Block'):
    for x in v['body']:run(x)
   elif n.kind=='VarDecl':env[v['name']]=ev(v['init']) if v['init'] else 0
   elif n.kind=='Assign':env[v['name']]=ev(v['expr'])
   elif n.kind=='Print':out.append(str(ev(v['expr'])))
   elif n.kind=='If':run(v['then'] if ev(v['cond']) else v['otherwise'])
   elif n.kind=='While':
    guard=0
    while ev(v['cond']):run(v['body']);guard+=1;assert guard<100000,'Loop limit reached'
   elif n.kind=='For':
    run(v['init']);guard=0
    while v['cond'] is None or ev(v['cond']):run(v['body']);run(v['update']);guard+=1;assert guard<100000,'Loop limit reached'
  run(ast);return out
