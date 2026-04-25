import unittest
from markdown_to_html import block_to_block_type, BlockType, markdown_to_blocks


class TestBlockType(unittest.TestCase):
    def test_blocktype1(self):
        block = "#### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_blocktype2(self):
        block = "```\ncode block\n```"

        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_blocktype3(self):
        block = "> quotes\n> quotes\n> quotes"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_blocktype4(self):
        block = "- item\n- item- item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_blocktype5(self):
        block = "1. item1\n2. item2\n3. item3\n4. item4"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_blocktype6(self):
        block = "1. item1\n2. item2\n3. item3\nitem4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_blocktype7(self):
        block = "```\ncode block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_blocktype8(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

1. This is an
2. ordered list
3. with items

> These are
> quotes

```
This is
a code block
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "1. This is an\n2. ordered list\n3. with items",
                "> These are\n> quotes",
                "```\nThis is\na code block\n```",
            ],
        )

        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.QUOTE,
                BlockType.CODE
            ]
        )