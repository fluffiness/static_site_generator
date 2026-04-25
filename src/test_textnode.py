import unittest
from textnode import TextNode, TextType
from textnode_utils import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq2(self):
        node1 = TextNode("A", TextType.BOLD)
        node2 = TextNode("B", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_eq2(self):
        node1 = TextNode("A", TextType.BOLD, "None")
        node2 = TextNode("A", TextType.TEXT, "None")
        self.assertNotEqual(node1, node2)
    
    def test_eq3(self):
        node1 = TextNode("A", TextType.TEXT, "None")
        node2 = TextNode("A", TextType.TEXT)
        self.assertNotEqual(node1, node2)
    
    def test_eq3(self):
        node1 = TextNode("A", TextType.TEXT, "None")
        node2 = TextNode("A", TextType.TEXT, "B")
        self.assertNotEqual(node1, node2)

    def test_eq3(self):
        node1 = TextNode("A", TextType.TEXT, "B")
        node2 = TextNode("A", TextType.TEXT, "B")
        self.assertEqual(node1, node2)
    
    def test_text_to_html1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html2(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_to_html3(self):
        node = TextNode("This is an image text node", TextType.IMAGE, url="path")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "path", "alt": "This is an image text node"})

    def test_text_to_html4(self):
        node = TextNode("This is a link text node", TextType.LINK, url="link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "link"})


if __name__ == "__main__":
    unittest.main()