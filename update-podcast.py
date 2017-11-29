#!/usr/bin/env python3
import sys
import os
import argparse
import requests

from datetime import datetime
from random import sample
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS

if sys.version_info.major == 2:
    from urlparse import urlparse
elif sys.version_info.major == 3:
    from urllib.parse import urlparse

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

def indent(elem, level=0):
    """with apologies to https://stackoverflow.com/a/33956544/3453874"""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def format_item(uri, book, chapter):
    today = datetime.strftime(datetime.today(), '%A, %d %b %Y %H:%M:%S')
    guid = ET.Element('guid')
    guid.text = uri
    link = ET.Element('link')
    link.text = uri
    title = ET.Element('title')
    title.text = '{0} {1}'.format(book, chapter)
    title.text = ' '.join([w.capitalize() for w in title.text.replace('-', ' ').split()])
    desc = ET.Element('description')
    desc.text = urlparse(uri).path.rsplit('/', 1)[-1]
    pub = ET.Element('pubDate')
    pub.text = today
    encl = ET.Element('enclosure', url=uri, type='audio/mpeg', length='0')
    item = ET.Element('item')
    item.append(guid)
    item.append(link)
    item.append(title)
    item.append(desc)
    item.append(pub)
    item.append(encl)
    return item

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
    with open('rss/{}.rss'.format(args.work),'r') as rss:
        tree = ET.parse(rss)
    root = tree.getroot()
    channel = root.find('channel')
    channel.append(format_item(uri, args.book, args.chapter))
    indent(root)
    tree.write('rss/{}.rss'.format(args.work))

