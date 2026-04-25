import os
import shutil 

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import copytree, extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dst_path):
    if not os.path.exists(from_path):
        raise ValueError(f"Markdown file not found at {from_path}")
    if not os.path.exists(template_path):
        raise ValueError(f"Template not found at {template_path}")
    
    print(f"Generating page from {from_path} to {dst_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace("{{ Content }}", content).replace("{{ Title }}", title)

    dest_parent = os.path.dirname(dst_path)
    if not os.path.exists(dest_parent):
        os.makedirs(dest_parent)

    with open(dst_path, 'w') as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dst_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"content directory not found at {dir_path_content}")
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"{dir_path_content} is not a directory")
    if not os.path.exists(template_path):
        raise ValueError(f"Template not found at {template_path}")
    
    os.makedirs(dst_dir_path, exist_ok=True)
    
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and os.path.splitext(item_path)[1] == ".md":
            html_item = os.path.splitext(item)[0] + ".html"
            dst_file_path = os.path.join(dst_dir_path, html_item)
            generate_page(item_path, template_path, dst_file_path)
        elif os.path.isdir(item_path):
            new_dst_dir_path = os.path.join(dst_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dst_dir_path)


def main():
    static_dir = "./static"
    public_dir = "./public"
    copytree(static_dir, public_dir)

    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "public"

    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


if __name__ == "__main__":
    main()