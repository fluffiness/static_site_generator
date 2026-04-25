import os
import shutil 

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import copytree, extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise ValueError("Markdown file not found")
    if not os.path.exists(template_path):
        raise ValueError("Template not found")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace("{{ Content }}", content).replace("{{ Title }}", title)

    dest_parent = os.path.dirname(dest_path)
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent)

    with open(dest_path, 'w') as f:
        f.write(html)


def main():
    static_dir = "./static"
    public_dir = "./public"
    copytree(static_dir, public_dir)

    markdown_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"

    generate_page(markdown_path, template_path, dest_path)


if __name__ == "__main__":
    main()