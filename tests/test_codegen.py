import unittest
from tinyc.lexer import tokenize
from tinyc.parser import Parser
from tinyc.codegen import Generator
class CodegenTests(unittest.TestCase):
 def test_interpreter(self):
  a=Parser(tokenize('print(2+3*4);')).parse(); self.assertEqual(Generator().run(a),['14'])
 def test_loop_result(self):
  a=Parser(tokenize('int i=0; for(i=0;i<3;i=i+1) print(i);')).parse(); self.assertEqual(Generator().run(a),['0','1','2'])
