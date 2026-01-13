import unittest
from block_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_md_to_blocks(self): 
        md_block = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md_block)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md_block = """
    This is block 1


    This is block 2

    """
        blocks = markdown_to_blocks(md_block)
        self.assertEqual(
            blocks,
            ["This is block 1", "This is block 2"],
        )

    def test_markdown_to_blocks_single(self):
        md = "Just a single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block of text."])

    def test_markdown_to_blocks_whitespace(self):
        md = "  This is a block with leading/trailing spaces   \n\n   Another block here  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a block with leading/trailing spaces", "Another block here"]
        )
    def test_block_to_block_types(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> quote\n> more quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("* list\n* item"), BlockType.U_L)
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.O_L)
        self.assertEqual(block_to_block_type("just a paragraph"), BlockType.PARAGRAPH)

    def test_ordered_list_fail(self):
        # Testing the sequence break logic you just implemented
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    def test_heading_fail(self):
        # Testing the regex fullmatch logic
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#no_space"), BlockType.PARAGRAPH)
        
if __name__ == "__main__":
    unittest.main()