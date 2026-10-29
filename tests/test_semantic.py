import unittest
from tinyc.lexer import tokenize
from tinyc.parser import Parser
from tinyc.semantic import Analyzer
class SemanticTests(unittest.TestCase):
 def test_undeclared(self):
  a=Analyzer().analyze(Parser(tokenize('print(x);')).parse()); self.assertTrue(a.errors)
 def test_scope_and_redeclaration(self):
  a=Analyzer().analyze(Parser(tokenize('int x; int x; { int x=1; }')).parse()); self.assertTrue(a.errors)
