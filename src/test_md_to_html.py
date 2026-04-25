import unittest
from markdown_to_html import markdown_to_html_node

class TestMd2HTML(unittest.TestCase):
    def test_md_to_html1(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_md_to_html2(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_md_to_html3(self):
        md = """
### Heading3

This is a
paragraph

```
This is text that _should_ remain
the **same** even with inline stuff
```

> This is
> a **block** quote

- These are
- items in an
- unordered list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                "<div><h3>Heading3</h3><p>This is a paragraph</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>"
                "<blockquote><p>This is a <b>block</b> quote</p></blockquote><ul><li>These are</li><li>items in an</li><li>unordered list</li></ul></div>"
            )
        )

    def test_md_to_html4(self):
        md = """
1. These are
2. items
3. in an
4. ordered list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>These are</li><li>items</li><li>in an</li><li>ordered list</li></ol></div>",
        )

    def test_md_to_html5(self):
        md = """
# Heading1

This is a paragraph
with **bold** text, _italic_ text,
and `inline code`.


"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading1</h1><p>This is a paragraph with <b>bold</b> text, <i>italic</i> text, and <code>inline code</code>.</p></div>",
        )