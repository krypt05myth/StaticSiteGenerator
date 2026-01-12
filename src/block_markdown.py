from textnode import TextNode, TextType

def markdown_to_blocks(md_block: str):
    md_block = md_block.split("\n\n")
    # md_block = md_block.strip()
    md_block_filtered = [item.strip() for item in md_block if item.strip() != ""]
    return md_block_filtered

## FOR INTERNAL-TO-FILE TESTING
# if __name__ == "__main__":
#     md_block = """This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items"""
#     md_block = md_block.strip()
#     md_block = md_block.split("\n")
#     md_block_filtered = [item for item in md_block if item]
#     print(md_block_filtered)