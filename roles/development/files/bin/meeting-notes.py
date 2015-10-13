#!/usr/bin/env python3

import time
import datetime

import requests

mon, tue, wed, thu, fri, sat, sun = range(7)

def last(day):
    today = datetime.date.today()
    offset = (today.weekday() + 6 - day) % 7
    return today - datetime.timedelta(days=offset)

last_wednesday = time.mktime(last(wed).timetuple())

datagrepper = 'https://apps.fedoraproject.org/datagrepper/raw'
response = requests.get(datagrepper, params=dict(
    topic='org.fedoraproject.prod.mailman.receive',
    contains='infrastructure',
    rows_per_page=100,
    start=last_wednesday,
))

data = response.json()
messages = data['raw_messages']

for message in messages:
    msg = message['msg']['msg']
    subject = msg['subject']
    author = msg['from'].split()[0]
    link = msg['archived-at'].strip('<>')
    print("#info %s - %s - %s" % (subject, author, link))
