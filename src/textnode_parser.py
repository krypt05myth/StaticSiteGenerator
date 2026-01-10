from textnode import TextNode, TextType
'''
class TextType(Enum):
    TEXT = "text"       # text (plain)
    BOLD = "bold"       # **Bold text**
    ITALIC = "italic"   # _Italic text_
    CODE = "code"       # `Code text`
    LINK = "link"       # [anchor text](url)
    IMAGE = "image"     # ![alt  text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
'''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_splitted = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes_splitted.append(node)
        temp = node.text.split(delimiter)
        # print(temp)
        if len(temp) % 2 == 0:
            raise ValueError("Valid Markdown has leading and trailing markers; this appears to be missing one side.")
        # we need to check each part of the temp list for its TextType and append to final list
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
