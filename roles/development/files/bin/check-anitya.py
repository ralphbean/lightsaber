#!/usr/bin/env python

import requests
import sys

if __name__ == '__main__':
    project = sys.argv[-1]

    anitya_url = 'https://release-monitoring.org'

    url = '%s/api/projects/?pattern=%s' % (anitya_url, project)
    response = requests.get(url)

    data = response.json()

    if data['total'] < 1:
        print "No project by the name of %r found." % project
        sys.exit(1)

    if data['total'] > 1:
        print "Name %r ambiguous, %r entries found." % (project, data['total'])
        sys.exit(2)

    # OK - then we found the project.  Now force a check.
    idx = data['projects'][0]['id']
    url = '%s/api/version/get' % anitya_url
    resp = requests.post(url, data=dict(id=idx))
    data = resp.json()

    if 'error' in data:
        print 'Anitya error: %r' % data['error']
        sys.exit(3)

    print "Check yielded upstream version %s for %s" % (
        data['version'], data['name'])

    if not any([p['distro'] == 'Fedora' for p in data['packages']]):
        print "WARN: Not mapped to Fedora."
        print "%s/project/%i" % (anitya_url, idx)
