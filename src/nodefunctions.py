import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # We don't support splitting nodes of any type besides text.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Make sure this is valid markdown.
        if (node.text.count("delimiter") % 2) > 0:
            raise Exception("Invalid markdown")

        # Split the text based on the given delimiter.
        substrs = node.text.split(delimiter)
        for i in range(0, len(substrs)):
            if len(substrs[i]) == 0:
                continue

            # Even-numbered substrings will always be outside the marked text.
            if i % 2 == 0:
                new_nodes.append(TextNode(substrs[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(substrs[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No title found")

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # We don't support splitting nodes of any type besides text.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract the markdown and add an appropriate node to the list.
        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            substrs = text.split(f"![{image[0]}]({image[1]})", 1)
            text = substrs[1]
            if len(substrs[0]) > 0:
                new_nodes.append(TextNode(substrs[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # We don't support splitting nodes of any type besides text.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract the markdown and add an appropriate node to the list.
        text = node.text
        links = extract_markdown_links(text)
        for link in links:
            substrs =   text.split(f"[{link[0]}]({link[1]})", 1)
            text = substrs[1]
            if len(substrs[0]) > 0:
                new_nodes.append(TextNode(substrs[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
