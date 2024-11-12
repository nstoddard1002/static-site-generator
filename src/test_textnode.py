import unittest
from textnode import TextNode, TextType

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
    

if __name__ == "__main__":
    unittest.main()
