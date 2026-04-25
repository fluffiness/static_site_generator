import os
import shutil


def copytree(src, dst):
    if not os.path.exists(src):
        raise ValueError("src does not exist")
    if not os.path.isdir(src):
        raise ValueError("src is not a directory")
    if os.path.exists(dst) and os.path.isdir(dst):
        shutil.rmtree(dst)
    
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        elif os.path.isdir(item_path):
            dst_item_dir = os.path.join(dst, item)
            copytree(item_path, dst_item_dir)


def extract_title(markdown: str) -> str:
    lines = markdown.split('\n')
    for line in lines:
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("Error: Title not found")