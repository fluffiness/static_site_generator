from typing import Optional, Self, Dict, List, Union

class HTMLNode:
    def __init__(
            self, 
            tag: Optional[str]=None, 
            value: Optional[str]=None, 
            children: Optional[List[Self]]=None, 
            props: Optional[Dict[str, str]]=None
        ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        props_str = ""
        if self.props:
            for k, v in self.props.items():
                props_str += f' {k}="{v}"'
        return props_str
    
    def __repr__(self) -> str:
        add_indent = lambda string: "    " + "\n      ".join(string.split('\n'))
        if not self.children:
            children_str = "[]"
        else:
            children_str = "[\n  " + "\n  ".join([add_indent(repr(child)) for child in self.children]) + "\n  ]"
        repr_str = f"HTMLNode(\n  tag={self.tag},\n  value={self.value}\n  children={children_str}\n  props={self.props_to_html()}\n)"
        return repr_str


class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: Union[str, None], 
            value: str, 
            props: Optional[Dict[str, str]]=None
        ):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Error: all leaf nodes must have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        repr_str = f"LeafNode(\n  tag={self.tag},\n  value={self.value}\n  props={self.props_to_html()}\n)"
        return repr_str


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: List[Self],
            props: Optional[Dict[str, str]]=None
        ):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("all parent nodes must have tags")
        if not self.children:
            raise ValueError("all parent nodes must have children")
        start_tag = f"<{self.tag}{self.props_to_html()}>"
        end_tag = f"</{self.tag}>"
        body = "".join([child.to_html() for child in self.children])
        return start_tag + body + end_tag
