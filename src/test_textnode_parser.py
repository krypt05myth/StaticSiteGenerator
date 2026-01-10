import unittest
from textnode import TextNode, TextType
from textnode_parser import split_nodes_delimiter

class TestHTMLNode(unittest.TestCase):
    def test_split_bold(self): 
        node = TextNode("This is text with a **BOLD** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_mismatch(self):
        node = TextNode("This _italicized is just normal. Woof.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()