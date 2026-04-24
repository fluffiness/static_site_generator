import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props1(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "a"})
        expected = ' href="https://www.google.com" target="a"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props2(self):
        node = HTMLNode(props={"a": "b", "c": "d"})
        expected = ' a="b" c="d"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props3(self):
        node = HTMLNode()
        expected = ''
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()