#!/usr/bin/env python

import fedora.client.bodhi

username = "ralph"

client = fedora.client.bodhi.Bodhi2Client()

print " * Making query against bodhi."
data = client.query(
    status="testing",
    user=username,
    limit=999,
)

link = lambda s: "https://bodhi.fedoraproject.org/updates/%s" % s

good, bad = [], []

# Scrape the comments to figure out what we can do.  :-x
for update in data['updates']:
    if update.request:
        continue
    if update.meets_testing_requirements:
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
