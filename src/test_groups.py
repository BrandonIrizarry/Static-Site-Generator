import unittest
import groups as src


class TestProcessWordGroup(unittest.TestCase):
    def test_simple_case(self):
        group = ["**", "This", "**"]
        processed = src.process_word_group(group)

        self.assertEqual(processed, "<b>This</b>")

        print(processed)
