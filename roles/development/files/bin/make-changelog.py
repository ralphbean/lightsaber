#!/usr/bin/env python
""" A script to generate a changelog from the git log.

"""

import argparse
import commands
import subprocess as sp
import sys

import requests

from distutils.version import LooseVersion

github_session = requests.session()

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
    tags.sort(key=LooseVersion)
    tags.append('develop')
    return list(reversed(tags))


def get_commits(start, stop):
    cmd = "git log {start}...{stop} --pretty=format:'%H %s' --reverse | cat"
    cmd = cmd.format(start=start, stop=stop)
    output = run(cmd)
    commits = [line.split(None, 1) for line in output]
    return commits


def commit_url_for(username, project, slug):
    template = "https://github.com/{username}/{project}/commit/{slug}"
    return template.format(username=username, project=project, slug=slug[:9])


def pull_url_for(username, project, number):
    template = "https://github.com/{username}/{project}/pull/{number}"
    return template.format(username=username, project=project, number=number)


def get_pull_info(username, project, number):
    template = 'https://api.github.com/repos/' + \
        '{username}/{project}/pulls/{number}'
    url = template.format(username=username, project=project, number=number)
    password = commands.getoutput('pass sites/github')
    response = github_session.get(url, auth=('ralphbean', password))
    body = response.json()
    title = body['title']
    author = body['user']['login']
    link = pull_url_for(username, project, number)
    return title, author, link


def main(username, project, version):

    tags = get_tags()

    # This would do all tags
    #for i in range(len(tags) - 1)

    # But we're just doing the first one now..
    for i in range(1):
        start, stop = tags[i], tags[i + 1]
        commits = get_commits(start, stop)

        if start == 'develop':
            start = version
            #commits = commits
        else:
            commits = commits[:-1]

        relstr = "Merge branch 'release"
        pullstr = "Merge pull request #"

        commits = [(slug, msg) for slug, msg in commits if relstr not in msg]
        pulls = [(slug, msg) for slug, msg in commits if pullstr in msg]
        commits = [(slug, msg) for slug, msg in commits if pullstr not in msg]

        print
        print start
        print "-" * len(start)

        if pulls:
            print
            print "Pull Requests"
            print

        for slug, msg in pulls:
            number = msg[len(pullstr):].split()[0]
            try:
                title, author, link = get_pull_info(username, project, number)
                author = "(@%s)" % author
            except KeyError as e:
                sys.stderr.write('Problems getting info for '
                                 '#%s\n%r\n' % (number, e))
                # Some fallbacks
                author = ''
                title = msg
                link = pull_url_for(username, project, number)

            print "- %s #%s, %s\n  %s" % (author.ljust(17), number, title, link)

        if commits:
            print
            print "Commits"
            print

        for slug, msg in commits:
            print "- %s %s\n  %s" % (
                slug[:9], msg, commit_url_for(username, project, slug))


if __name__ == '__main__':
    args = parse_args()
    main(username=args.username, project=args.project, version=args.version)
