import unittest

from nodefunctions import *
from textnode import TextNode, TextType


class TestNodeFunctions(unittest.TestCase):
    def test_split_nontext_node(self):
        results = split_nodes_delimiter(
            [TextNode("This is a bold node", TextType.BOLD)],
            "_",
            TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("This is a bold node", TextType.BOLD)
            ],
            results
        )

    def test_split_text_node_beginning(self):
        results = split_nodes_delimiter(
            [TextNode("**This** is a bold node", TextType.TEXT)],
            "**",
            TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a bold node", TextType.TEXT)
            ],
            results
        )

    def test_split_text_node_middle(self):
        results = split_nodes_delimiter(
            [TextNode("This is a **bold** node", TextType.TEXT)],
            "**",
            TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" node", TextType.TEXT)
            ],
            results
        )

    def test_split_text_node_end(self):
        results = split_nodes_delimiter(
            [TextNode("This is a bold **node**", TextType.TEXT)],
            "**",
            TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This is a bold ", TextType.TEXT),
                TextNode("node", TextType.BOLD)
            ],
            results
        )

    def test_split_text_node_multiple_instances(self):
        results = split_nodes_delimiter(
            [TextNode("**This** is a **bold** node", TextType.TEXT)],
            "**",
            TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" node", TextType.TEXT)
            ],
            results
        )

    def test_split_multiple_text_nodes(self):
        results = split_nodes_delimiter(
            [
                TextNode("This is a `code` node", TextType.TEXT),
                TextNode("And another code `node`", TextType.TEXT)
            ],
            "`",
            TextType.CODE)
        
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.TEXT),
                TextNode("And another code ", TextType.TEXT),
                TextNode("node", TextType.CODE)
            ],
            results
        )

    def test_extract_single_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_single_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )

        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                )
            ],
            new_nodes
        )
