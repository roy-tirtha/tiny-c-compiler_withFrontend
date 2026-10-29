"""CLI and compile API."""
import argparse,json,sys,time
from pathlib import Path
from .lexer import tokenize
from .parser import Parser
from .semantic import Analyzer
from .codegen import Generator
from .errors import CompilerError
def compile_source(source):
 r={'success':False,'stages':{},'trace':[],'errors':[]};step=0
 def emit(file,function,message,data):
  nonlocal step;step+=1;r['trace'].append({'step':step,'stage':file[:-3],'file':file,'function':function,'message':message,'data':data})
 def run(name,fn):
  start=time.perf_counter()
  try:o=fn();r['stages'][name]={'status':'done','duration_ms':round((time.perf_counter()-start)*1000,2),'output':o};return o
  except Exception:r['stages'][name]={'status':'failed','duration_ms':round((time.perf_counter()-start)*1000,2),'output':None};raise
 try:
  tokens=run('lexer',lambda:tokenize(source,emit));r['stages']['lexer']['output']=[x.to_dict() for x in tokens]
  ast=run('parser',lambda:Parser(tokens,source,emit).parse());r['stages']['parser']['output']=ast.to_dict()
  analyzer=Analyzer(emit);sem=run('semantic',lambda:analyzer.analyze(ast));r['stages']['symbol_table']={'status':'done','duration_ms':0,'output':{'operations':sem.symbols.operations}};r['stages']['semantic']['output']={'errors':sem.errors,'warnings':sem.warnings}
  if sem.errors:
   r['errors']=[{'stage':'semantic','file':'semantic.py','snippet':source.splitlines()[e['line']-1] if source.splitlines() else '', 'hint':'Declare the name in this scope or choose a different name.',**e} for e in sem.errors];return r
  gen=Generator(emit);tac=run('codegen',lambda:gen.generate(ast));r['stages']['codegen']['output']={'tac':tac,'program_output':gen.run(ast)};r['success']=True
 except CompilerError as e:r['errors']=[e.to_dict()]
 except Exception as e:r['errors']=[{'stage':'internal','file':'main.py','message':str(e),'line':1,'column':1,'snippet':'','hint':'Review this program and retry.'}]
 for n in ('lexer','parser','symbol_table','semantic','codegen'):r['stages'].setdefault(n,{'status':'skipped','duration_ms':0,'output':None})
 return r
def main():
 p=argparse.ArgumentParser();p.add_argument('file',nargs='?');p.add_argument('--tokens',action='store_true');p.add_argument('--ast',action='store_true');p.add_argument('--symbols',action='store_true');p.add_argument('--tac',action='store_true');p.add_argument('--run',action='store_true');p.add_argument('--serve',action='store_true');a=p.parse_args()
 if a.serve:
  from .server import serve;serve();return
 source=Path(a.file).read_text() if a.file else sys.stdin.read();r=compile_source(source);print(json.dumps(r,indent=2));raise SystemExit(0 if r['success'] else 1)
if __name__=='__main__':main()
