import re
from typing import List, Tuple
from htmlnode import LeafNode
from textnode import TextNode, TextType


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
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        num_delimiters_found = 0
        remainder = node.text
        while delimiter in remainder:
            num_delimiters_found += 1
            segment, remainder = remainder.split(delimiter, maxsplit=1)
            if segment:
                if num_delimiters_found % 2 == 1:
                    new_nodes.append(TextNode(segment, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))
        
        if num_delimiters_found % 2 != 0:
            raise Exception("Error: Invalid Markdown syntax. Unmatched delimiter found")
        
        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images_found = extract_markdown_images(node.text)
        remainder = node.text
        for alt_text, src in images_found:
            md_image = f"![{alt_text}]({src})"
            preceding_text, remainder = remainder.split(md_image, maxsplit=1)
            if preceding_text:
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, src))
        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links_found = extract_markdown_links(node.text)
        remainder = node.text
        for link_text, url in links_found:
            md_link = f"[{link_text}]({url})"
            preceding_text, remainder = remainder.split(md_link, maxsplit=1)
            if preceding_text:
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes