import unittest
from markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_with_extra_newlines(self):
        text = "# Header\n\n\n\nThis is a paragraph.\n\n\n* Bullet point\n\nAnother paragraph with extra newlines."
        result = markdown_to_blocks(text)
        expected = [
            "# Header",
            "This is a paragraph.",
            "* Bullet point",
            "Another paragraph with extra newlines."
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_empty_string(self):
        text = ""
        result = markdown_to_blocks(text)
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_with_only_newlines(self):
        text = "\n\n\n\n"
        result = markdown_to_blocks(text)
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_single_block(self):
        text = "This is a single paragraph block without any extra newlines."
        result = markdown_to_blocks(text)
        expected = ["This is a single paragraph block without any extra newlines."]
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_multiple_paragraphs(self):
        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three with some **bold** text."
        result = markdown_to_blocks(text)
        expected = [
            "Paragraph one.",
            "Paragraph two.",
            "Paragraph three with some **bold** text."
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_mixed_content(self):
        text = "# Header\n\nThis is a paragraph.\n\n- Bullet item\n- Another bullet item\n\n1. Numbered item\n2. Another numbered item\n\n**Bold block**\n\n`Code block`"
        result = markdown_to_blocks(text)
        expected = [
            "# Header",
            "This is a paragraph.",
            "- Bullet item\n- Another bullet item",
            "1. Numbered item\n2. Another numbered item",
            "**Bold block**",
            "`Code block`"
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()