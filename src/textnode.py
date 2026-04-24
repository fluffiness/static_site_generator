from enum import Enum
from typing import Self, Optional

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str]=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: Self):
        same_text = self.text == other.text
        same_text_type = self.text_type.value == other.text_type.value
        same_url = other.url is None if self.url is None else self.url == other.url
        return same_text and same_text_type and same_url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"