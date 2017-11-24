#!/usr/bin/env python3
import sys
from datetime import datetime
import xml.etree.ElementTree as ET

def indent(elem, level=0):
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

def format_item(arg):
    today = datetime.strftime(datetime.today(), '%A, %d %b %Y %H:%M:%S')
    uri = 'http://192.168.200.22:8080/{}'.format(arg)
    guid = ET.Element('guid')
    guid.text = uri
    link = ET.Element('link')
    link.text = uri
    title = ET.Element('title')
    title.text = arg
    desc = ET.Element('description')
    desc.text = arg
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
    if len(sys.argv) > 1:
        with open('rss/scripture-podcast.rss','r') as rss:
            tree = ET.parse(rss)
        root = tree.getroot()
        channel = root.find('channel')
        for arg in sys.argv[1:]:
            print("Arg received: {}".format(arg))
            channel.append(format_item(arg))
        indent(root)
        tree.write('rss/scripture-podcast.rss')

