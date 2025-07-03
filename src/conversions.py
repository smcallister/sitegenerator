from enum import Enum

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from nodefunctions import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Nodes of type link must have a url defined")

            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Nodes of type image must have a url defined")

            return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text
                })

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_htmlnodes(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))

def markdown_to_blocks(markdown):
    blocks = []
    substrs = markdown.split("\n\n")
    for substr in substrs:
        substr = substr.strip()
        if len(substr) > 0:
            blocks.append(substr)
    
    return blocks

def block_to_block_type(markdown):
    # Check for heading blocks.
    if markdown.startswith("#") and not markdown.startswith("#######"):
        return BlockType.HEADING

    # Check for code blocks.
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    # Check for quote blocks and lists. Start by determining the type of the first line.
    if markdown.startswith(">"):
        block_type = BlockType.QUOTE
    elif markdown.startswith("- "):
        block_type = BlockType.UNORDERED_LIST
    elif markdown.startswith("1. "):
        block_type = BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

    lines = markdown.split('\n')
    for i in range(1, len(lines)):
        match block_type:
            case BlockType.QUOTE:
                if not lines[i].startswith(">"):
                    return BlockType.PARAGRAPH

            case BlockType.UNORDERED_LIST:
                if not lines[i].startswith("- "):
                    return BlockType.PARAGRAPH

            case BlockType.ORDERED_LIST:
                if not lines[i].startswith(f"{i + 1}. "):
                    return BlockType.PARAGRAPH
    
    return block_type

def block_to_html_node(markdown):
    block_type = block_to_block_type(markdown)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_htmlnodes(markdown.replace("\n", " ")))
        
        case BlockType.HEADING:
            depth = 0
            for c in markdown:
                if c == "#":
                    depth += 1
                else:
                    break
            
            return ParentNode(f"h{depth}", text_to_htmlnodes(markdown[depth + 1:]))

        case BlockType.CODE:
            code_node = text_node_to_html_node(TextNode(markdown.replace("```", "").lstrip(), TextType.CODE))
            return ParentNode("pre", [code_node])

        case BlockType.QUOTE:
            return ParentNode("blockquote", text_to_htmlnodes(markdown.replace("> ", "").replace(">", "").replace("\n", " ")))

        case BlockType.UNORDERED_LIST:
            children = []
            lines = markdown.split('\n')
            for line in lines:
                children.append(ParentNode("li", text_to_htmlnodes(line[2:])))

            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            children = []
            lines = markdown.split('\n')
            for line in lines:
                children.append(ParentNode("li", text_to_htmlnodes(line[3:])))
                
            return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root = ParentNode("div", [])

    for block in blocks:
        node = block_to_html_node(block)
        root.children.append(node)
    
    return root
