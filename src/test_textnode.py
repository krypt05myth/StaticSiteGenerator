import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

##my attempt at some tests
    def test_assert_equal(self):
        node1 = TextNode("My assert equal test.", TextType.ITALIC)
        node2 = TextNode("My assert equal test.", TextType.ITALIC)
        self.assertEqual(node1, node2, msg="Must be equal.")

    def test_assert_not_equal(self):
        node1 = TextNode("My assert not equal test; node1", TextType.BOLD)
        node2 = TextNode("My assert not equal test; node2", TextType.ITALIC)
        self.assertNotEqual(node1, node2, msg="Must not be equal.")

    def test_missing_url(self):
        node1 = TextNode("My missing url test", TextType.BOLD, url='test.url')
        node2 = TextNode("My missing url test", TextType.BOLD, url=None)
        self.assertNotEqual(node1, node2, msg="Must be missing url.")

    def test_textType_not_equal(self):
        node1 = TextNode("My textType mixup.", TextType.BOLD, url='test.url')
        node2 = TextNode("My textType mixup.", TextType.ITALIC, url='test.url')
        self.assertNotEqual(node1, node2, msg="Must be a textType mixup.")

if __name__ == "__main__":
    unittest.main()
