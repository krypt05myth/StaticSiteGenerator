import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
##my attempt at some tests
    def test_defaults(self):
        # Testing that initial values are None if not provided
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "some.site"})
        expected_prop = ' href="some.site"'
        self.assertEqual(node.props_to_html(), expected_prop)
    
    def test_props_to_html_many_prop(self):
        node = HTMLNode(props={"href": "some.site", "target": "nothing"})
        expected_props = ' href="some.site" target="nothing"'
        self.assertEqual(node.props_to_html(), expected_props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_link(self):
        node = LeafNode("a", "Underlined Link Here", {"href": "some.site"})
        self.assertEqual(node.to_html(), '<a href="some.site">Underlined Link Here</a>')

    def test_leaf_no_tag_raw_text(self):
        node = LeafNode(None, "Just text, no tag")
        self.assertEqual(node.to_html(), "Just text, no tag")
    
    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
