import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.leaf2 = LeafNode("a", "Click me!", {"span", "child"})
        self.leaf3 = LeafNode("code", "grandchild")

        self.parent1 = ParentNode("span", [self.leaf3])
        self.parent2 = ParentNode("div", [self.parent1])
        self.parent3 = ParentNode("p", [self.parent2])

        self.parent4 = ParentNode("p", [self.leaf1])
        self.parent5 = ParentNode("body", [self.parent3, self.parent4])

    def test1(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test2(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test3(self):
        self.assertEqual(
            self.parent3.to_html(),
            "<p><div><span><code>grandchild</code></span></div></p>"
        )

    def test4(self):
        self.assertEqual(
            self.parent5.to_html(),
            '<body><p><div><span><code>grandchild</code></span></div></p><p><a href="https://www.google.com">Click me!</a></p></body>'
        )

