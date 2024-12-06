import unittest
import groups as src


class TestProcessWordGroup(unittest.TestCase):
    def test_simple_case(self):
        group = ["**", "This", "**"]
        processed = src.process_word_group(group)

        self.assertEqual(processed, "<b>This</b>")

        print(processed)

    def test_multiple_simple_cases(self):
        group = ["This", "**", "is", "**", "a", "*", "line", "*", ":", "`", "hello", "world", "`"]
        processed = src.process_word_group(group)

        # Note that this represents a slight bug in our program.
        self.assertEqual("This <b>is</b> a <i>line</i> : <code>hello world</code>", processed)
