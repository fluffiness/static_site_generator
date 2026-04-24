from enum import Enum
from typing import Self, Optional, List
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str]=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: Self) -> bool:
        same_text = self.text == other.text
        same_text_type = self.text_type.value == other.text_type.value
        same_url = other.url is None if self.url is None else self.url == other.url
        return same_text and same_text_type and same_url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        else:
            num_delimiters_found = 0
            remainder = node.text
            while delimiter in remainder:
                num_delimiters_found += 1
                segment, remainder = remainder.split(delimiter, maxsplit=1)
                if num_delimiters_found % 2 == 1:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))
            
            if num_delimiters_found % 2 != 0:
                raise Exception("Error: Invalid Markdown syntax. Unmatched delimiter found")
            
            if remainder:
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes
                

    