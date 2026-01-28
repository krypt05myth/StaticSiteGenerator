import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"      # Standard text block
    HEADING = "heading"          # Starts with 1-6 '#' characters
    QUOTE = "quote"              # Every line starts with '>'
    CODE = "code"                # Block starts and ends with '```'
    U_L = "unordered_list"       # Every line starts with '*' or '-'
    O_L = "ordered_list"         # Lines start with '1.', '2.', etc.

def markdown_to_blocks(md: str):
    md = md.split("\n\n")
    # md_block = md_block.strip()
    md_filtered = [block.strip() for block in md if block.strip() != ""]
    return md_filtered # from a 'block' of md to a list of str from the 'block' str

def block_to_block_type(md: str):
    # HEADING
    if md.startswith("#"):
        if re.match(r"(?<!#)#{1,6}\s", md):
            return BlockType.HEADING
    # CODE
    if md.startswith("```") and md.endswith("```"):
        return BlockType.CODE
    # QUOTE
    if md.startswith(">"):
        lines = md.splitlines()
        if all(line.startswith(">") for line in lines): ## <- GENERATOR EXPR SYNTAX!!!
            return BlockType.QUOTE
    # UNORDERED_LIST
    if md.startswith(("* ", "- ")): ## A "LOGICAL OR TUPLE" IS TOTALLY FINE TO PASS IN!!
        lines = md.splitlines()
        if all(line.startswith(("* ", "- ")) for line in lines):
            return BlockType.U_L
    # ORDERED_LIST 
    if md.startswith("1. "):
        lines = md.splitlines()
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                # So, basically if even a single line fails the numbering sequence, it's a paragraph!
                return BlockType.PARAGRAPH
        return BlockType.O_L
    # PARAGRAPH -- DEFAULT
    return BlockType.PARAGRAPH

def extract_title(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        block_stripped = block.strip() # Want to catch the stray leading space, leniency allows only one fat-finger leading space! 
        # print(f"DEBUG: Checking block: '{block_stripped}' \nType: {block_to_block_type(block_stripped)} \n")
        if block_to_block_type(block_stripped) == BlockType.HEADING:
            if block_stripped.startswith("# "):
                return block_stripped.removeprefix("# ").strip()
    raise Exception("There is no H1 header.")

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