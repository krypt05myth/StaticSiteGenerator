import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

    ## LEAF NODE TESTS
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
    ## PARENT NODE TESTS
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_kids(self):
        kid = None
        parent = ParentNode("someTag", []) #empty list is where a 'kid' would be
        self.assertEqual(parent.to_html(), "<someTag></someTag>")

    def test_to_html_no_tag(self):
        kid = LeafNode("someTag", "someValue")
        parent = ParentNode(None, [kid])
        with self.assertRaises(ValueError):
            parent.to_html()

if __name__ == "__main__":
    unittest.main()
