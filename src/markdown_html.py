import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode, LeafNode, text_node_to_html_node
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes

def text_to_children_helper(block): ## Bridges gap from TNodes to HNodes
    block_tnodes = text_to_textnodes(block) # eg: [TextNode("This is ", TextType.TEXT), TextNode("bold", TextType.BOLD)]
    tnodes2html = [] # final list will be eg: [LeafNode(None, text_node.text), LeafNode("b", text_node.text)]
    for ea in block_tnodes:
         tnodes2html.append(text_node_to_html_node(ea)) # appends some kinda LN: LeafNode("b", text_node.text)
    return tnodes2html

def block_to_html_node_helper(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        normalized_text = " ".join(block.splitlines()) # lines need to be collapsed - \n becomes \s
        return ParentNode("p", text_to_children_helper(normalized_text)) # wraps list of inline html in 'p' tag
    elif block_type == BlockType.HEADING:
        hash_tags = re.match(r"((?<!#)#{1,6})", block) # capture the leading hash tags in the block
        if hash_tags:
            h_level = len(hash_tags.group(1)) # .group is how we refers to the capture group
            return ParentNode(f"h{h_level}", text_to_children_helper(block[h_level + 1:]))
        else:
            raise Exception("Heading misidentified or misconfigured. Check hash tags notation.")
    elif block_type == BlockType.CODE:
        stripped = block.strip("`").strip("\n")
        tnode = TextNode(stripped, TextType.TEXT) #manual create TN with stripped/cleaned TEXT
        hnode = text_node_to_html_node(tnode) #manual create HN from that TN
        code_node = ParentNode("code", [hnode]) #manual created internal portion of a CODE node
        return ParentNode("pre", [code_node]) #return the final, external, wrapped "pre" node
    elif block_type == BlockType.QUOTE:
        split_strip = " ".join([line.strip('>').strip() for line in block.splitlines()]) #must splitlines 1st, then strip each, then join back!
        return ParentNode("blockquote", text_to_children_helper(split_strip))
    elif block_type == BlockType.U_L:
        splitted = block.splitlines() #must splitlines 1st
        kid_wrapped = []
        for ea in splitted:
            sliced = ea[2:] # because it will start with either "* " or "- ", and we need that removed!
            children = text_to_children_helper(sliced) #makes a list of html LN kids
            kid_wrapped.append(ParentNode("li",children)) #PN because inside each <li> could be <b>, <i>, etc LNs!
        return ParentNode("ul", kid_wrapped) 
    elif block_type == BlockType.O_L:
        splitted = block.splitlines() #must splitlines 1st
        kid_wrapped = []
        for ea in splitted:
            dotted = ea.find(". ") # .find returns the INDEX of the 1st ch (".") in the pattern ". "
            sliced = ea[dotted + 2:] # because it will start with either "1. ", "2. ", "{#}. ", and we need that removed!
            children = text_to_children_helper(sliced) #makes a list of html LN kids
            kid_wrapped.append(ParentNode("li",children)) #PN because inside each <li> could be <b>, <i>, etc LNs!
        return ParentNode("ol", kid_wrapped) 

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md) # from big ole md text file to a bunch of blocks (strs) in a list
    kids = []
    for block in blocks:
        kid = block_to_html_node_helper(block) # sent to fn to basically find the block type, construct proper html node
        kids.append(kid)
    return ParentNode("div", kids)


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

'''
THIS IS FOR REFERENCE OF ANOTHER WAY THAT I COULD'VE SOLVED IT -- PERHAPS CLEANER?!
'''
# import re
# from htmlnode import ParentNode, LeafNode
# from textnode import text_node_to_html_node
# from inline_markdown import text_to_textnodes
# from block_markdown import (
#     BlockType,
#     markdown_to_blocks,
#     block_to_block_type,
# )

# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     children = []
#     for block in blocks:
#         html_node = block_to_html_node(block)
#         children.append(html_node)
#     return ParentNode("div", children)

# def block_to_html_node(block):
#     block_type = block_to_block_type(block)
#     if block_type == BlockType.QUOTE:
#         return create_quote_node(block)
#     if block_type == BlockType.U_L:
#         return create_unordered_list_node(block)
#     if block_type == BlockType.O_L:
#         return create_ordered_list_node(block)
#     if block_type == BlockType.CODE:
#         return create_code_node(block)
#     if block_type == BlockType.HEADING:
#         return create_heading_node(block)
#     if block_type == BlockType.PARAGRAPH:
#         return create_paragraph_node(block)
#     raise ValueError("Invalid block type")

# def text_to_children(text):
#     text_nodes = text_to_textnodes(text)
#     children = []
#     for text_node in text_nodes:
#         html_node = text_node_to_html_node(text_node)
#         children.append(html_node)
#     return children

# def create_paragraph_node(block):
#     lines = block.split("\n")
#     paragraph = " ".join(lines)
#     children = text_to_children(paragraph)
#     return ParentNode("p", children)

# def create_heading_node(block):
#     level = 0
#     for char in block:
#         if char == "#":
#             level += 1
#         else:
#             break
#     if level + 1 >= len(block):
#         raise ValueError(f"Invalid heading level: {level}")
#     text = block[level + 1 :]
#     children = text_to_children(text)
#     return ParentNode(f"h{level}", children)

# def create_code_node(block):
#     if not block.startswith("```") or not block.endswith("```"):
#         raise ValueError("Invalid code block")
#     # Slice off the backticks and any immediate leading/trailing newlines
#     text = block[3:-3].strip("\n")
#     # Use a LeafNode directly to avoid inline parsing (bold/italic)
#     code = LeafNode("code", text)
#     return ParentNode("pre", [code])

# def create_quote_node(block):
#     lines = block.split("\n")
#     new_lines = []
#     for line in lines:
#         if not line.startswith(">"):
#             raise ValueError("Invalid quote block")
#         new_lines.append(line.lstrip(">").strip())
#     content = " ".join(new_lines)
#     children = text_to_children(content)
#     return ParentNode("blockquote", children)

# def create_unordered_list_node(block):
#     items = block.split("\n")
#     html_items = []
#     for item in items:
#         text = item[2:]
#         children = text_to_children(text)
#         html_items.append(ParentNode("li", children))
#     return ParentNode("ul", html_items)

# def create_ordered_list_node(block):
#     items = block.split("\n")
#     html_items = []
#     for item in items:
#         # Matches '1. ', '2. ', etc.
#         pos = item.find(". ") + 2
#         text = item[pos:]
#         children = text_to_children(text)
#         html_items.append(ParentNode("li", children))
#     return ParentNode("ol", html_items)