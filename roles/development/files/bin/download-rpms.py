#!/usr/bin/env python
""" Downloads rpms from a koji task.

Kind of like 'koji download-build' except:

    1) it is standalone
    2) it works on tasks, not just builds.

Author: Ralph Bean <rbean@redhat.com>

"""

import bs4
import os
import requests
import sys
import urllib

idx = sys.argv[-1]
int(idx)  # Be sure its an int.

prefix = '/var/tmp/ralph-rpms'

template = 'http://koji.fedoraproject.org/koji/taskinfo?taskID={idx}'
response = requests.get(template.format(idx=idx))

soup = bs4.BeautifulSoup(response.text)

anchors = soup.findAll('a')
for anchor in anchors:
    href = anchor['href']
    if href.endswith('.rpm'):
        filename = os.path.join(prefix, href.split('/')[-1])
        print "* Downloading", href
        print "  to", filename
        urllib.urlretrieve(href, filename)
