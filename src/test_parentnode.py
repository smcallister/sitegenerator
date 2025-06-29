import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_one_child(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("span", "child")])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_childen(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("span", "child 1"),
                LeafNode("b", "child 2")
            ])

        self.assertEqual(parent_node.to_html(), "<div><span>child 1</span><b>child 2</b></div>")

    def test_to_html_with_single_grandchild(self):
        parent_node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "grandchild")
                    ]
                )
            ]
            )

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_grandchildren(self):
        parent_node = ParentNode(
            "div",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "grandchild 1"),
                        LeafNode("i", "grandchild 2")
                    ]
                ),
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "grandchild 3"),
                        LeafNode("i", "grandchild 4")
                    ]
                )               
            ]
        )

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild 1</b><i>grandchild 2</i></span><span><b>grandchild 3</b><i>grandchild 4</i></span></div>",
        )

    def test_to_html_with_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "child")])
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_no_children(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)
