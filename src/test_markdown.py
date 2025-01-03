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

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# Heading"
        result = block_to_blocktype(block)
        self.assertEqual(result,"heading")
    
    def test_code_block(self):
        block = "```\nprint('Hello, world!')\n```"
        result = block_to_blocktype(block)
        self.assertEqual(result,"code")

    def test_quote_block(self):
        block = ">This is a quote\n>Continued quote"
        result = block_to_blocktype(block)
        self.assertEqual(result,"quote")

    def test_unordered_list_block(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        result = block_to_blocktype(block)
        self.assertEqual(result,"unordered list")

    def test_unordered_list_alt_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_blocktype(block)
        self.assertEqual(result,"unordered list")

    def test_unordered_list_mixed_block(self):
        block = "* Item 1\n- Item 2\n* Item 3\n- Item 4"
        result = block_to_blocktype(block)
        self.assertEqual(result,"unordered list")

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_blocktype(block)
        self.assertEqual(result,"ordered list")

    def test_paragraph_block(self):
        block = "This is paragraph with multiple lines.\nThis is the second line."
        result = block_to_blocktype(block)
        self.assertEqual(result,"paragraph")

    def test_wrong_heading_block(self):
        block = "##There is no space after the # symbol"
        result = block_to_blocktype(block)
        self.assertEqual(result,"paragraph")
    
    def test_more_than_one_heading_block(self):
        block = "# There is too many lines\n# Even if they are formatted correctly"
        result = block_to_blocktype(block)
        self.assertEqual(result,"paragraph")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_HTMLNode(markdown)
        result = html_node.to_html()
        expected = "<div><p>This is a paragraph.</p></div>"
        self.assertEqual(result, expected)

    def test_heading(self):
        markdown = "# Heading 1"
        html_node = markdown_to_HTMLNode(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>Heading 1</h1></div>")

    def test_code_block(self):
        markdown = "```\nprint('Hello, World!')\n```"
        html_node = markdown_to_HTMLNode(markdown)
        self.assertEqual(html_node.to_html(), "<div><code>print('Hello, World!')</code></div>")

    def test_quote_block(self):
        markdown = "> This is a quote.\n> Continued quote."
        html_node = markdown_to_HTMLNode(markdown)
        self.assertEqual(html_node.to_html(), "<div><quote>This is a quote. Continued quote.</quote></div>")

    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        html_node = markdown_to_HTMLNode(markdown)
        self.assertEqual(html_node.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n3. Item 3"
        html_node = markdown_to_HTMLNode(markdown)
        self.assertEqual(html_node.to_html(), "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>")

if __name__ == "__main__":
    unittest.main()