import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class SourceTests(unittest.TestCase):
    def test_example_is_lazy_and_uses_neutral_credentials(self):
        source = (ROOT / "examples/openai_compat.py").read_text(encoding="utf-8")
        self.assertIn("OPENAI_API_KEY", source)
        self.assertIn("max_retries=0", source)
        self.assertNotIn("OpenAI(", source.split("def _client", 1)[0])

    def test_prompt_validation_is_offline(self):
        namespace = {}
        exec((ROOT / "examples/openai_compat.py").read_text(encoding="utf-8"), namespace)
        with self.assertRaises(ValueError):
            namespace["complete"](" ")


if __name__ == "__main__":
    unittest.main()
