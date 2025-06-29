import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_with_link(self):
        node = TextNode("This is a text node with a link", TextType.LINK, "http://localhost")
        node2 = TextNode("This is a text node with a link", TextType.LINK, "http://localhost")
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a different text node", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_neq_link(self):
        node = TextNode("This is a text node with a link", TextType.LINK, "http://localhost")
        node2 = TextNode("This is a text node with a link", TextType.LINK, "https://localhost")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(f'{node}', 'TextNode(This is a text node, bold, None)')
    
    def test_repr_with_link(self):
        node = TextNode("This is a text node with a link", TextType.LINK, "http://localhost")
        self.assertEqual(f'{node}', 'TextNode(This is a text node with a link, link, http://localhost)')

if __name__ == "__main__":
    unittest.main()