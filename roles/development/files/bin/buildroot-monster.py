#!/usr/bin/env python
""" Take a list of packages as arguments.

Print a giant shell oneliner to be executed by the user that generates buildroot
overrides for all the latest builds of all the packages passed in.

"""

import sh
import sys
import pprint

if __name__ == '__main__':
    builds = set()
    packages = sys.argv[1:]
    for package in packages:
        print "Querying %r" % package
        output = sh.bodhi(latest=package)
        for line in output.strip().split('\n'):
            print "\t%r" % line.strip()
            root, build = line.strip().split('  ')
            if 'testing' in root or 'candidate' in root:
                builds.add(build)

    print "-" * 20
    pprint.pprint(builds)
    print "-" * 20
    notes = raw_input("Notes: ")
    print "-" * 20

    tmpl = "bodhi --user ralph --notes=\"{notes}\" --buildroot-override={nvra} --duration=20"
    print " &&\\\n".join([tmpl.format(nvra=build, notes=notes)
                          for build in sorted(list(builds))])
