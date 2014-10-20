#!/usr/bin/env python
""" A script to generate a changelog from the git log.

"""

import argparse
import subprocess as sp
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default=None,
                        help="GitHub owner of the repo")
    parser.add_argument("--project", default=None,
                        help="Name of the Github repo")
    parser.add_argument("--version", default=None,
                        help="New version being released")

    args = parser.parse_args()

    if not args.username:
        sys.stderr.write("A username must be provided.\n")
        sys.exit(1)

    if not args.project:
        sys.stderr.write("A project must be provided.\n")
        sys.exit(1)

    if not args.version:
        sys.stderr.write("A version must be provided.\n")
        sys.exit(1)

    return args


def run(cmd):
    proc = sp.Popen([cmd], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    output = proc.communicate()[0]
    return output.strip().split('\n')


def get_tags():
    cmd = "git tag -l"
    tags = run(cmd)
    tags.append('develop')
    return list(reversed(tags))


def get_commits(start, stop):
    cmd = "git log {start}...{stop} --pretty=format:'%H %s' --reverse | cat"
    cmd = cmd.format(start=start, stop=stop)
    output = run(cmd)
    commits = [line.split(None, 1) for line in output]
    return commits


def url_for(username, project, slug):
    template = "https://github.com/{username}/{project}/commit/{slug}"
    return template.format(username=username, project=project, slug=slug)


def main(username, project, version):

    tags = get_tags()

    print "Changelog"
    print "========="

    for i in range(len(tags) - 1):
        start, stop = tags[i], tags[i + 1]
        commits = get_commits(start, stop)

        if start == 'develop':
            start = version
            #commits = commits
        else:
            commits = commits[:-1]

        print
        print start
        print "-" * len(start)
        print

        for slug, msg in commits:
            if "Merge branch 'release" in msg:
                continue
            print "- %s `%s <%s>`_" % (
                msg, slug[:9], url_for(username, project, slug))


if __name__ == '__main__':
    args = parse_args()
    main(username=args.username, project=args.project, version=args.version)
