import unittest
from tinyc.lexer import tokenize
class LexerTests(unittest.TestCase):
 def test_tokens_and_locations(self):
  t=tokenize('int x = 42; // hi\nprint(x);'); self.assertEqual(t[0].type,'INT'); self.assertEqual(t[3].lexeme,'42'); self.assertEqual(t[-1].type,'EOF'); self.assertEqual(t[-1].line,2)
 def test_comments_and_illegal_character(self):
  self.assertEqual(tokenize('/* x */ print(1);')[0].type,'PRINT')
  from tinyc.errors import LexicalError
  with self.assertRaises(LexicalError): tokenize('@')
