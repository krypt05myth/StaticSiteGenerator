# from htmlnode import HTMLNode, ParentNode, LeafNode
# from textnode import (
#     TextType,
#     TextNode,
#     LeafNode,
# )
# from block_markdown import (
#     BlockType,
#     markdown_to_blocks,
#     block_to_block_type,
# )
# import inline_markdown
# import re

# def block_to_html_node(block):
#     block_type = block_to_block_type(block)
#     if block_type == BlockType.PARAGRAPH:
#         # for now, just return *some* paragraph node, even without inline parsing
#         return ParentNode("p", [LeafNode(None, block)])
#     # handle other block types later

# def markdown_to_html_node(md):
#     blocks = markdown_to_blocks(md)
#     block_type = ""
#     kids = []
#     for block in blocks:
#         # tag_from_type = block_to_block_type(block)
#         kid = block_to_html_node(block)
#         kids.append(kid)
#     return ParentNode("div", kids)


# ## FOR INTERNAL-TO-FILE TESTING
# if __name__ == "__main__":
#     md_block = """This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items"""
#     node = markdown_to_html_node(md_block)
#     html = node.to_html()
#     self.assertEqual(
#         html,
#         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
#     )


import re
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.U_L:
        return create_unordered_list_node(block)
    if block_type == BlockType.O_L:
        return create_ordered_list_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_code_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    # Slice off the backticks and any immediate leading/trailing newlines
    text = block[3:-3].strip("\n")
    # Use a LeafNode directly to avoid inline parsing (bold/italic)
    code = LeafNode("code", text)
    return ParentNode("pre", [code])

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_unordered_list_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def create_ordered_list_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        # Matches '1. ', '2. ', etc.
        pos = item.find(". ") + 2
        text = item[pos:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)