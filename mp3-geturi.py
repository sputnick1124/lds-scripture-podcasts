#!/usr/bin/env python3
import sys
import argparse
from random import sample

import requests
if sys.version_info.major == 2:
    from urlparse import urlparse
elif sys.version_info.major == 3:
    from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS

def get_uri(work, book, chapter):
    uri = 'https://lds.org/scriptures/{0}/{1}/{2}'.format(work,book,chapter)
    page = requests.get(uri)
    parse = BS(page.text, 'html.parser')
    options = []
    for a in parse.findAll('a'):
        if a('downloadlabel'):
            options.append(a['href'])
    mp3_uri = urlparse(sample(options, 1)[0])
    return '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=mp3_uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='download the audio of argument from lds.org')
    parser.add_argument(
                'work', nargs='?',
                default='bofm',
                help='[ot|nt|bofm|pgp|dc]', type=str)
    parser.add_argument(
                'book',
                help='book from chosen work', type=str)
    parser.add_argument(
                'chapter',
                help='chapter from book', type=str)

    args = parser.parse_args()
    uri = get_uri(args.work, args.book, args.chapter)
    print(uri)

