#!/usr/bin/env python3

import collections
import time
import datetime

import requests

mon, tue, wed, thu, fri, sat, sun = range(7)

def last(day):
    today = datetime.date.today()
    offset = (today.weekday() + 6 - day) % 7
    return today - datetime.timedelta(days=offset)

last_wednesday = time.mktime(last(thu).timetuple())

def place_child(container, message):
    """ Recursively try to place a child message with its parent. """
    if not message['in-reply-to']:
        return False
    if message['in-reply-to'] in container:
        container[message['in-reply-to']]['children'][message['message-id']] = message
        return True
    for parent_id, parent in container.items():
        if place_child(parent['children'], message):
            return True
    return False

def print_tree(tree, depth=0):
    """ Recursively print out a tree of responses. """
    prefix = "#info"
    if depth:
        prefix = " " * len(prefix) + "  " * depth

    for idx, msg in tree.items():
        subject = msg['subject']
        author = msg['from'].split()[0]
        link = msg['archived-at'].strip('<>')
        print("%s %s - %s - %s" % (prefix, subject, author, link))
        print_tree(msg['children'], depth + 1)

if __name__ == '__main__':
    datagrepper = 'https://apps.fedoraproject.org/datagrepper/raw'
    response = requests.get(datagrepper, params=dict(
        topic='org.fedoraproject.prod.mailman.receive',
        contains='infrastructure',
        rows_per_page=100,
        start=last_wednesday,
        order='asc',
    ))

    data = response.json()
    original_messages = data['raw_messages']
    threaded_messages = collections.OrderedDict()

    for message in original_messages:
        msg = message['msg']['msg']
        msg['children'] = collections.OrderedDict()
        if not place_child(threaded_messages, msg):
            threaded_messages[msg['message-id']] = msg

    print_tree(threaded_messages)
