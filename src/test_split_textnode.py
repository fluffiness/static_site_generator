import unittest
from textnode import TextNode, TextType
from textnode_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_split_delimiters1(self):
        node = TextNode("This is a **bold** text node", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_split_delimiters2(self):
        node = TextNode("This is a _italic_ text node", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), expected)

    def test_split_delimiters3(self):
        node = TextNode("This is a `code` text node", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_delimiters4(self):
        node = TextNode("This is a **very** very **bold** text node", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" very ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)
    
    def test_split_delimiters5(self):
        node = TextNode("This is a **very** very **bold** text **node", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" very ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        with self.assertRaises(Exception) as e:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        print(str(e.exception))
    
    def test_extract_images1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_images2(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). "
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_extract_links1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_links1(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). "
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_images1(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT
            )
        ]
        expected = [
            TextNode(
                "This is text with a ",
                TextType.TEXT
            ),
            TextNode(
                "rick roll",
                TextType.IMAGE,
                "https://i.imgur.com/aKaOqIh.gif"
            ),
            TextNode(
                " and ",
                TextType.TEXT
            ),
            TextNode(
                "obi wan",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT
            )
        ]
        self.assertEqual(split_nodes_image(nodes), expected)
    
    def test_extract_markdown_images2(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
                TextType.TEXT
            )
        ]
        expected = [
            TextNode(
                "This is text with a ",
                TextType.TEXT
            ),
            TextNode(
                "rick roll",
                TextType.IMAGE,
                "https://i.imgur.com/aKaOqIh.gif"
            ),
            TextNode(
                " and ",
                TextType.TEXT
            ),
            TextNode(
                "obi wan",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(
                ".",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
                TextType.TEXT
            )
        ]
        self.assertEqual(split_nodes_image(nodes), expected)
    
    def test_extract_markdown_links1(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT
            )
        ]
        expected = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link ",
                TextType.TEXT
            ),
            TextNode(
                "to boot dev",
                TextType.LINK,
                "https://www.boot.dev"
            ),
            TextNode(
                " and ",
                TextType.TEXT
            ),
            TextNode(
                "to youtube",
                TextType.LINK,
                "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertEqual(split_nodes_link(nodes), expected)
    
    def test_extract_markdown_links1(self):
        nodes = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
                TextType.TEXT
            )
        ]
        expected = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).",
                TextType.TEXT
            ),
            TextNode(
                "This is text with a link ",
                TextType.TEXT
            ),
            TextNode(
                "to boot dev",
                TextType.LINK,
                "https://www.boot.dev"
            ),
            TextNode(
                " and ",
                TextType.TEXT
            ),
            TextNode(
                "to youtube",
                TextType.LINK,
                "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(
                ".",
                TextType.TEXT
            ),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)
    
    def test_text_to_textnodes1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes2(self):
        text = "This is a **text** with two **bold** words, two _italic_ words _and_ a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with two ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words, two ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words ", TextType.TEXT),
            TextNode("and", TextType.ITALIC),
            TextNode(" a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)




if __name__ == "__main__":
    unittest.main()