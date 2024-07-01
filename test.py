#!/usr/bin/env python3

import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)

import unittest
from purifyurl import extract_urls, clean_url, expand_url, clean_urls

class TestPurifyURL(unittest.TestCase):

    def test_extract_urls(self):
        text = "Visit http://example.com and https://www.example.com for more info."
        expected = ["http://example.com", "https://www.example.com"]
        result = extract_urls(text)
        self.assertEqual(result, expected)

    def test_clean_url(self):
        url = "https://www.youtube.com/watch?v=xyz&si=test"
        cleaner = lambda x: x
        expected = "https://www.youtube.com/watch?v=xyz"
        result = clean_url(url, cleaner)
        self.assertEqual(result, expected)

    def test_expand_url(self):
        url = "https://tinyurl.com/example"
        expected = "https://www.example.com"
        result = expand_url(url)
        self.assertEqual(result, expected)

    def test_clean_urls(self):
        urls = ["http://example.com?utm_source=google"]
        cleaner = lambda x: x.replace("?utm_source=google", "")
        expected = ["http://example.com"]
        result = clean_urls(urls, cleaner)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

