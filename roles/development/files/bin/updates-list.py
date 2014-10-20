#!/usr/bin/env python

import datetime
import getpass
import fedora.client.bodhi

client = fedora.client.bodhi.BodhiClient(
    username="ralph",
)
client.password = getpass.getpass()

print " * Making query against bodhi."
data = client.query(
    status="testing",
    mine=True,
    limit=999,
)

then = datetime.datetime.now() - datetime.timedelta(days=14)
parse = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
link = lambda s: "https://admin.fedoraproject.org/updates/%s" % s

good, bad = [], []

for update in data['updates']:
    if parse(update.date_pushed) < then:
        good.append(update)
    else:
        bad.append(update)

def print_title(title):
    print
    print '-' * len(title)
    print title
    print '-' * len(title)

print_title("these are not ready to be pushed")

for update in bad:
    print " -", update.karma, link(update.title)

print_title("these should be good to go")

for update in good:
    print " +", update.karma, link(update.title)
