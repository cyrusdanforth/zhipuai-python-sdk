import pathlib,unittest
class T(unittest.TestCase):
 def test_neutral_key(self):
  s=pathlib.Path("examples/openai_compat.py").read_text();self.assertIn("OPENAI_API_KEY",s)
if __name__=='__main__':unittest.main()
