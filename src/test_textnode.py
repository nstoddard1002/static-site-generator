import unittest
from textnode import TextNode, TextType, split_nodes_delimiter

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



if __name__ == "__main__":
    unittest.main()
