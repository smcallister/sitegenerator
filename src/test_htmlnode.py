import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_none(self):
        node = HTMLNode("p", "Some Text")
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(
            "a",
            "Local Host",
            None,
            {
                "href": "http://localhost"
            })
        self.assertEqual(node.props_to_html(), 'href="http://localhost"')

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            "a",
            "Local Host",
            None,
            {
                "href": "http://localhost",
                "target": "_blank"
            })
        self.assertEqual(node.props_to_html(), 'href="http://localhost" target="_blank"')
