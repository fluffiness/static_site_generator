from typing import List
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from textnode_utils import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    for n in range(1, 7):
        heading_start = '#' * n + ' '
        if block[: n + 1] == heading_start:
            return BlockType.HEADING
    
    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    
    lines = block.split('\n')

    is_quote = True
    is_unordered = True
    is_ordered = True
    for i, line in enumerate(lines):
        if not is_quote or not line.startswith('>'):
            is_quote = False
        if not is_unordered or not line.startswith('-'):
            is_unordered = False
        if not is_ordered or not line.startswith(f"{i+1}."):
            is_ordered = False

    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def paragraph_to_html_node(block: str) -> ParentNode:
    block_inline = ' '.join([line.strip() for line in block.split('\n')])
    block_text_nodes = text_to_textnodes(block_inline)
    block_leaf_nodes = [text_node_to_html_node(text_node) for text_node in block_text_nodes]
    return ParentNode(tag='p', children=block_leaf_nodes)


def heading_to_html_node(block: str) -> ParentNode:
    hashes, heading_text = block.split(' ', maxsplit=1)
    tag = f"h{len(hashes)}"
    block_text_nodes = text_to_textnodes(heading_text)
    block_leaf_nodes = [text_node_to_html_node(text_node) for text_node in block_text_nodes]
    return ParentNode(tag=tag, children=block_leaf_nodes)


def code_to_html_node(block: str) -> ParentNode:
    code_text = block[4:-3]
    block_text_node = TextNode(text=code_text, text_type=TextType.TEXT)
    block_leaf_nodes = [text_node_to_html_node(block_text_node)]
    code_node = ParentNode(tag="code", children=block_leaf_nodes)
    return ParentNode(tag="pre", children=[code_node])


def quote_to_html_node(block: str) -> ParentNode:
    quote_lines = [line[2:] for line in block.split('\n')]
    quote_text = ' '.join(quote_lines)
    block_text_nodes = text_to_textnodes(quote_text)
    block_leaf_nodes = [text_node_to_html_node(text_node) for text_node in block_text_nodes]
    return ParentNode(tag="blockquote", children=block_leaf_nodes)


def unordered_list_to_html_node(block: str) -> ParentNode:
    quote_lines = [line[2:] for line in block.split('\n')]
    items_html_nodes = []
    for line in quote_lines:
        line_text_nodes = text_to_textnodes(line)
        line_leaf_nodes = [text_node_to_html_node(text_node) for text_node in line_text_nodes]
        item_html_node = ParentNode(tag="li", children=line_leaf_nodes)
        items_html_nodes.append(item_html_node)
    return ParentNode(tag="ul", children=items_html_nodes)


def ordered_list_to_html_node(block: str) -> ParentNode:
    quote_lines = [line[3:] for line in block.split('\n')]
    items_html_nodes = []
    for line in quote_lines:
        line_text_nodes = text_to_textnodes(line)
        line_leaf_nodes = [text_node_to_html_node(text_node) for text_node in line_text_nodes]
        item_html_node = ParentNode(tag="li", children=line_leaf_nodes)
        items_html_nodes.append(item_html_node)
    return ParentNode(tag="ol", children=items_html_nodes)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    block_nodes= []
    for block, block_type in zip(blocks, block_types):
        match block_type:
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                block_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                block_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                block_nodes.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                block_nodes.append(ordered_list_to_html_node(block))
    return ParentNode(tag="div", children=block_nodes)


    