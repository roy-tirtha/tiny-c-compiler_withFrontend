import unittest
from tinyc.lexer import tokenize
from tinyc.parser import Parser
class ParserTests(unittest.TestCase):
 def test_precedence_tree(self):
  a=Parser(tokenize('print(2+3*4);')).parse(); e=a.values['body'][0].values['expr']; self.assertEqual(e.values['op'],'+')
 def test_for_loop(self):
  a=Parser(tokenize('for (int i=0;i<2;i=i+1) print(i);')).parse(); self.assertEqual(a.values['body'][0].kind,'For')
