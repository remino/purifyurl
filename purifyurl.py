#!/usr/bin/env python3

import sys
import re
import argparse
import urllib.parse
from url_cleaner import UrlCleaner
import requests

def extract_urls(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)

def expand_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Error expanding URL {url}: {e}", file=sys.stderr)
        return url

def clean_url(url, cleaner):
    cleaned_url = cleaner(url)
    parsed_url = urllib.parse.urlparse(cleaned_url)
    qs = urllib.parse.parse_qs(parsed_url.query)
    if parsed_url.netloc in ["youtube.com", "www.youtube.com"]:
        qs.pop("si", None)
    new_query = urllib.parse.urlencode(qs, doseq=True)
    new_url = parsed_url._replace(query=new_query).geturl()
    return new_url

def clean_urls(urls, cleaner):
    return [clean_url(url, cleaner) for url in urls]

def replace_urls(text, url_map):
    for original, cleaned in url_map.items():
        text = text.replace(original, cleaned)
    return text

def main():
    parser = argparse.ArgumentParser(description='Clean URLs from tracking parameters.')
    parser.add_argument('urls', nargs='*', help='URLs to be cleaned')
    parser.add_argument('-e', '--expand', action='store_true', help='Expand shortened URLs')
    parser.add_argument('-u', '--update', action='store_true', help='Update url_cleaner rules')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    cleaner = UrlCleaner()
    
    if args.update:
        cleaner.ruler.update_rules()
        print("Rules updated.")
        return

    if args.urls:
        urls = args.urls
    else:
        input_data = sys.stdin.read()
        urls = extract_urls(input_data)

    cleaned_urls = urls
    
    if args.expand:
        cleaned_urls = clean_urls(urls, cleaner.clean)
        cleaned_urls = [expand_url(url) for url in cleaned_urls]
    
    cleaned_urls = clean_urls(cleaned_urls, cleaner.clean)
        
    url_map = dict(zip(urls, cleaned_urls))

    if args.urls:
        for url in cleaned_urls:
            print(url)
    else:
        modified_input = replace_urls(input_data, url_map)
        print(modified_input, end='')

if __name__ == "__main__":
    main()

