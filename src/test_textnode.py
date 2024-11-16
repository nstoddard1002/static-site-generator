import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)
    
    def test_neq(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3,node4)

    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD,"http://url.com")
        node2 = TextNode("This is different text", TextType.CODE)
        self.assertNotEqual(node,node2)
    
class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_single_delimiter(self):
        nodes = [TextNode("Hello, **bold** world!", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes,"**",TextType.BOLD)
        expected = [
            TextNode("Hello, ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" world!", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_delimiters(self):
        nodes = [TextNode("**Bold** and _italic_ text", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        expected = [
            TextNode("Bold",TextType.BOLD),
            TextNode(" and ",TextType.NORMAL),
            TextNode("italic",TextType.ITALIC),
            TextNode(" text",TextType.NORMAL)
        ]
        self.assertEqual(result,expected)

    def test_no_delimiter(self):
        nodes = [TextNode("Plain text with no formatting", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes,"**",TextType.BOLD)
        expected = [TextNode("Plain text with no formatting", TextType.NORMAL)]
        self.assertEqual(result,expected)

    def test_text_ends_with_delimiter(self):
        nodes = [TextNode("Bold at the end**",TextType.NORMAL)]
        result = split_nodes_delimiter(nodes,"**",TextType.BOLD)
        expected = [TextNode("Bold at the end",TextType.NORMAL)]
        self.assertEqual(result,expected)

    def test_empty_text(self):
        nodes = [TextNode("",TextType.NORMAL)]
        result = split_nodes_delimiter(nodes,"**",TextType.BOLD)
        expected = [TextNode("",TextType.NORMAL)]
        self.assertEqual(result,expected)

class TextExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is an image: ![Sample Image](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("Sample Image", "https://example.com/image.png")]
        self.assertEqual(result, expected)
    
    def test_multiple_images(self):
        text = "![First Image](https://example.com/first.png) and ![Second Image](https://example.com/second.png)"
        result = extract_markdown_images(text)
        expected = [
            ("First Image", "https://example.com/first.png"),
            ("Second Image", "https://example.com/second.png")
        ]
        self.assertEqual(result, expected)

    def test_image_no_matches(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

class TextExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Check out this [link](https://example.com)!"
        result = extract_markdown_links(text)
        expected = [("link","https://example.com")]
        self.assertEqual(result, expected)
    
    def test_multiple_links(self):
        text = "[Google](https://google.com) and [Bing](https://bing.com)"
        result = extract_markdown_links(text)
        expected = [
            ("Google","https://google.com"),
            ("Bing","https://bing.com")
        ]
        self.assertEqual(result, expected)

    def test_link_no_matches(self):
        text = "This text has no links"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

class TextExtractImagesAndLinks(unittest.TestCase):
    def test_images_and_links_mixed(self):
        text = "![Image](https://example.com/image.png) and [Link](https://example.com)"

        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)

        expected_images = [("Image","https://example.com/image.png")]
        expected_links = [("Link","https://example.com")]

        self.assertEqual(image_result,expected_images)
        self.assertEqual(link_result,expected_links)

class TestSplitImageNodes(unittest.TestCase):

    def test_single_image(self):
        nodes = [TextNode("Here is an image: ![Sample Image](https://example.com/image.png)", TextType.NORMAL)]
        result = split_nodes_images(nodes)
        expected = [
            TextNode("Here is an image: ", TextType.NORMAL),
            TextNode("Sample Image", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        nodes = [TextNode("![First Image](https://example.com/first.png) and ![Second Image](https://example.com/second.png)", TextType.NORMAL)]
        result = split_nodes_images(nodes)
        expected = [
            TextNode("First Image", TextType.IMAGE, "https://example.com/first.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Second Image", TextType.IMAGE, "https://example.com/second.png")
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_nodes_with_single_images(self):
        nodes = [
            TextNode("Here is an image: ![Sample Image](https://example.com/image.png)", TextType.NORMAL, url=None),
            TextNode("Here is an image: ![Sample Image](https://example.com/image.png)", TextType.NORMAL, url=None)
        ]
        result = split_nodes_images(nodes)
        expected = [
            TextNode("Here is an image: ", TextType.NORMAL),
            TextNode("Sample Image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("Here is an image: ", TextType.NORMAL),
            TextNode("Sample Image", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes_with_multiple_images(self):
        nodes = [
            TextNode("![First Image](https://example.com/first.png) and ![Second Image](https://example.com/second.png)", TextType.NORMAL),
            TextNode("![First Image](https://example.com/first.png) and ![Second Image](https://example.com/second.png)", TextType.NORMAL)
        ]
        result = split_nodes_images(nodes)
        expected = [
            TextNode("First Image", TextType.IMAGE, "https://example.com/first.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Second Image", TextType.IMAGE, "https://example.com/second.png"),
            TextNode("First Image", TextType.IMAGE, "https://example.com/first.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Second Image", TextType.IMAGE, "https://example.com/second.png")
        ]
        self.assertEqual(result, expected)

    def test_without_images(self):
        nodes = [TextNode("This text has no images.", TextType.NORMAL)]
        result = split_nodes_images(nodes)
        expected = [TextNode("This text has no images.", TextType.NORMAL)]
        self.assertEqual(result, expected)

class TestSplitLinkNodes(unittest.TestCase):
    
    def test_single_link(self):
        nodes = [TextNode("Check out this [link](https://example.com)!", TextType.NORMAL)]
        result = split_nodes_links(nodes)
        expected = [
            TextNode("Check out this ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("!",TextType.NORMAL)
        ]
        self.assertEqual(result,expected)

    def test_multiple_links(self):
        nodes = [TextNode("[Google](https://google.com) and [Bing](https://bing.com)", TextType.NORMAL)]
        result = split_nodes_links(nodes)
        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Bing", TextType.LINK, "https://bing.com")
        ]
        self.assertEqual(result, expected)

    def test_text_without_links(self):
        nodes = [TextNode("This text has no links", TextType.NORMAL)]
        result = split_nodes_links(nodes)
        expected = [TextNode("This text has no links", TextType.NORMAL)]
        self.assertEqual(result, expected)
    
    def test_multple_nodes_with_single_links(self):
        nodes = [
            TextNode("Check out this [link](https://example.com)!", TextType.NORMAL),
            TextNode("Check out this [link](https://example.com)!", TextType.NORMAL)
        ]
        result = split_nodes_links(nodes)
        expected = [
            TextNode("Check out this ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("!",TextType.NORMAL),
            TextNode("Check out this ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("!",TextType.NORMAL)
        ]
        self.assertEqual(result,expected)
    
    def test_multiple_nodes_with_multiple_links(self):
        nodes = [
            TextNode("[Google](https://google.com) and [Bing](https://bing.com)", TextType.NORMAL),
            TextNode("[Google](https://google.com) and [Bing](https://bing.com)", TextType.NORMAL)
        ]
        result = split_nodes_links(nodes)
        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("Bing", TextType.LINK, "https://bing.com")
        ]
        self.assertEqual(result, expected)

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text."
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text.",TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)
    
    def test_code_text(self):
        text = "This is `code` text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_combined_bold_italic_text(self):
        text = "This is **bold** and *italic* text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_image_text(self):
        text = "Here is an image: ![Sample Image](https://example.com/sample.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an image: ", TextType.NORMAL),
            TextNode("Sample Image", TextType.IMAGE, "https://example.com/sample.png")
        ]
        self.assertEqual(result, expected)

    def test_link_text(self):
        text = "Check out this [link](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)
    
    def test_combined_formatting(self):
        text = "This is *italic*, **bold**, and `code` text as well as [a link](https://example.com) and ![an image](https://example.com/image.png)!!"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text as well as ", TextType.NORMAL),
            TextNode("a link", TextType.LINK,"https://example.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("an image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("!!", TextType.NORMAL)
        ]
        self.assertEqual(result,expected)

if __name__ == "__main__":
    unittest.main()
