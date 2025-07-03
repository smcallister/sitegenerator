import unittest

from conversions import *
from textnode import TextNode, TextType


class TestConversions(unittest.TestCase):
    def test_text_conversion_with_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_node_conversion_with_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_node_conversion_with_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_node_conversion_with_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_node_conversion_with_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://localhost")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "http://localhost")

    def test_node_conversion_with_link_no_link(self):
        node = TextNode("This is a link node", TextType.LINK)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_node_conversion_with_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://localhost/hello.gif")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "http://localhost/hello.gif")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "This is an image node")

    def test_node_conversion_with_image_no_link(self):
        node = TextNode("This is an image node", TextType.IMAGE)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_with_heading(self):
        md = """# This is a heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_with_invalid_heading(self):
        md = """####### This is an invalid heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_code(self):
        md = """``` This is a code block ```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_with_invalid_code(self):
        md = """``` This is an invalid code block"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_quote(self):
        md = """> This is a quote block
> with a second line
>
> and a third line"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_with_invalid_quote(self):
        md = """> This is a quote block
> with a second line
and a third line"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_unordered_list(self):
        md = """- This is an unordered list
- with a second item
- and a third item"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_with_invalid_unordered_list(self):
        md = """- This is an unordered list
- with a second item
-and a third item"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_ordered_list(self):
        md = """1. This is an ordered list
2. with a second item
3. and a third item"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_with_invalid_ordered_list(self):
        md = """1. This is an ordered list
2. with a second item
3.and a third item"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_out_of_order_list(self):
        md = """1. This is an ordered list
2. with a second item
4. and a third item"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote block
> with a **bolded** word
> and a word in _italics_.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block with a <b>bolded</b> word and a word in <i>italics</i>.</blockquote></div>",
        )

    def test_unordered_lists(self):
        md = """
- This is the first item in an unordered list.
- This is the second item.
- This is the third item.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the first item in an unordered list.</li><li>This is the second item.</li><li>This is the third item.</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """
1. This is the first item in an ordered list.
2. This is the second item.
3. This is the third item.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first item in an ordered list.</li><li>This is the second item.</li><li>This is the third item.</li></ol></div>",
        )