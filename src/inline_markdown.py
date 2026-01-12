import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    # The r prefix makes it a 'raw' string so backslashes aren't eaten by Python
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
'''
1 - !\[ <--"Find exactly ![." (This is the start marker for images).
2 - ( <--"Start saving what follows into Group 1."
3 - [^\]]* <--"Keep grabbing every character until you hit a ]." (Everything until syntax is [^]* <--square brackets and caret and asterisk)
4 - ) <--"Stop saving to Group 1."
5 - \] <--"Match the literal ]." (This is the end marker for the alt-text).
'''

def extract_markdown_links(text):
    # This uses a 'negative lookbehind' (?<!!) to ensure we don't catch images
    # Positive lookback is (?<=)  <- not that in both, parents included!
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            image_alt = image[0]
            image_url = image[1]
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_splitted = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_splitted.append(node)
            continue # this prevents the node from being processed twice!
        temp = node.text.split(delimiter)
        # print(temp)
        if len(temp) % 2 == 0:
            raise ValueError("Valid Markdown has leading and trailing markers; this appears to be missing one side.")
        # need to check each part of the temp list for its TextType and append to final list
        for i in range(len(temp)):
            if temp[i] == "":
                continue
            if i % 2 == 0:
                new_nodes_splitted.append(TextNode(temp[i], TextType.TEXT))
            else:
                new_nodes_splitted.append(TextNode(temp[i], text_type))
    return new_nodes_splitted

## FOR INTERNAL-TO-FILE TESTING
# if __name__ == "__main__":
#     node = TextNode("This is text with a `code block` word", TextType.TEXT)
#     new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#     print(new_nodes)
