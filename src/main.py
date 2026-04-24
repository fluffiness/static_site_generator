from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    leaf2 = LeafNode("a", "Click me!", {"span", "child"})
    leaf3 = LeafNode("code", "grandchild")

    parent1 = ParentNode("span", [leaf3])
    parent2 = ParentNode("div", [parent1])
    parent3 = ParentNode("p", [parent2])

    parent4 = ParentNode("p", [leaf1])
    parent5 = ParentNode("body", [parent3, parent4])

    print(parent5.to_html())



if __name__ == "__main__":
    main()