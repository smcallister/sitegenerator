import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
    
    def test_to_html_with_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), 'Hello, world!')

    def test_to_html_with_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_a(self):
        node = LeafNode(
            "a",
            "Local Host",
            {
                "href": "http://localhost",
                "target": "_blank"
            })
        self.assertEqual(node.to_html(), '<a href="http://localhost" target="_blank">Local Host</a>')