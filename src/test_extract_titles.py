import unittest
from utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title1(self):
        md = """
# heading1

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        title = extract_title(md)
        self.assertEqual(title, "heading1")

    def test_extract_title2(self):
        md = """

        
# Hello world!!

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        title = extract_title(md)
        self.assertEqual(title, "Hello world!!")