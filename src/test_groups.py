import unittest
import groups as src


class TestProcessWordGroup(unittest.TestCase):
    def test_simple_case(self):
        group = ["**", "This", "**"]
        processed = src.process_word_group(group)

        self.assertEqual(processed, "<b>This</b>")


    def test_without_markup(self):
        group = ['In', ' ', 'the', ' ', 'beginning.']
        expected = "In the beginning."
        actual = src.process_word_group(group)

        self.assertEqual(expected, actual)


    def test_multiple_simple_cases(self):
        group = [
            'This', ' ', 'is', ' ', 'a', ' ', 'paragraph', ' ', 'of', ' ',
            'text.', ' ', 'It', ' ', 'has', ' ', 'some', ' ', '**', 'bold',
            '**', ',', ' ', 'and', ' ', '*', 'italic', '*', ',', ' ', 'words...'
        ]

        processed = src.process_word_group(group)

        # Note that this represents a slight bug in our program.
        self.assertEqual("This is a paragraph of text. It has some <b>bold</b>, and <i>italic</i>, words...", processed)


    def test_mapping_over_list(self):
        groups = [
            ['This', ' ', 'is', ' ', 'a', ' ', 'paragraph', ' ', 'of', ' ', 'text.',
             ' ', 'It', ' ', 'has', ' ', 'some', ' ', '**', 'bold', '**', ',', ' ', 'and',
             ' ', '*', 'italic', '*', ',', ' ', 'words'],
            ['inside', ' ', 'of', ' ', 'it.', ' ', 'This', ' ', 'is', ' ', 'more', ' ', 'of',
             ' ', 'the', ' ', '*', 'same', ' ', 'paragraph', '*', '.', ' ', 'This', ' ', 'is', ' ', 'to', ' ',
             'prove', ' ', 'the'],
            ['point', ' ', 'that', ' ', 'paragraphs', ' ', 'can', ' ', 'span', ' ', 'multiple',
             ' ', 'lines.']
        ]

        actual = list(map(src.process_word_group, groups))
        expected = [
            "This is a paragraph of text. It has some <b>bold</b>, and <i>italic</i>, words",
            "inside of it. This is more of the <i>same paragraph</i>. This is to prove the",
            "point that paragraphs can span multiple lines."
        ]

        self.assertEqual(expected, actual)


    def test_nested_inline_styles(self):
        sentence = "Dillinger is a cloud-enabled, <i>mobile-<b>ready</b></i> , offline-storage compatible..."
        splitted = src.split_keep_whitespace(sentence)
        tokenized = src.tokenize_inline_style_markers(splitted)
        rejoined = src.process_word_group(tokenized)

        expected = "Dillinger is a cloud-enabled, <i>mobile-<b>ready</b></i> , offline-storage compatible..."
        self.assertEqual(expected, rejoined)
