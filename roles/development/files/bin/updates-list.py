#!/usr/bin/env python

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

link = lambda s: "https://admin.fedoraproject.org/updates/%s" % s

good, bad = [], []

# Scrape the comments to figure out what we can do.  :-x
for update in data['updates']:
    if update.request:
        continue
    for comment in update.comments:
        if 'can be pushed to stable now' in comment.text:
            good.append(update)
            break
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
