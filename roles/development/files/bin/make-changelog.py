#!/usr/bin/env python
""" A script to generate a changelog from the git log.

"""

import argparse
import commands
import subprocess as sp
import sys

import arrow
import requests

from distutils.version import LooseVersion

github_session = requests.session()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default=None,
                        help="Owner of the repo for projects on GitHub")
    parser.add_argument("--project", default=None,
                        help="Name of the project")
    parser.add_argument("--version", default=None,
                        help="New version being released")
    parser.add_argument("--pagure", default=False, action='store_true',
                        help="Flag to use for pagure projects")

    args = parser.parse_args()

    if not args.username and not args.pagure:
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
    if 'develop' in run('git branch'):
        tags.append('develop')
    return list(reversed(tags))


def get_commits(start, stop):
    cmd = "git log {start}...{stop} --pretty=format:'%H %ci %s' --reverse | cat"
    cmd = cmd.format(start=start, stop=stop)
    output = run(cmd)
    commits = []
    for line in output:
        line = line.split(None, 4)
        commits.append([line[0], ' '.join(line[1:4]), line[4]])
    return commits


def commit_url_for_github(username, project, slug):
    template = "https://github.com/{username}/{project}/commit/{slug}"
    return template.format(username=username, project=project, slug=slug[:9])


def commit_url_for_pagure(project, slug):
    template = "https://pagure.io/{project}/{slug}"
    return template.format(project=project, slug=slug[:9])


def pull_url_for_github(username, project, number):
    template = "https://github.com/{username}/{project}/pull/{number}"
    return template.format(username=username, project=project, number=number)


def pull_url_for_pagure(project, number):
    template = "https://pagure.io/{project}/pull-request/{number}"
    return template.format(project=project, number=number)


def get_pull_info_github(username, project, number):
    template = 'https://api.github.com/repos/' + \
        '{username}/{project}/pulls/{number}'
    url = template.format(username=username, project=project, number=number)
    password = commands.getoutput('pass sites/github')
    response = github_session.get(url, auth=('ralphbean', password))
    body = response.json()
    title = body['title']
    author = body['user']['login']
    link = pull_url_for_github(username, project, number)
    return title, author, link


def get_pull_info_pagure(username, project, number):
    template = 'https://pagure.io/api/0/{project}/pull-request/{number}'
    url = template.format(project=project, number=number)
    response = github_session.get(url)
    body = response.json()
    title = body['title']
    author = body['user']['name']
    link = pull_url_for_pagure(project, number)
    return title, author, link


def get_pull_request_pagure(project, commit):
    commit_date = arrow.get(commit[1])
    template = 'https://pagure.io/api/0/{project}/pull-requests?status=Merged'
    url = template.format(project=project)
    response = github_session.get(url)
    body = response.json()
    requests = []
    for request in body.get('requests', []):
        req_update = arrow.get(
            request.get('updated_on', request['date_created'])
        )
        if req_update > commit_date:
            requests.append([
                request['id'], request['title'], request['user']['name']
            ])

    return requests


def main(username, project, version, pagure=False):

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

        if pagure:
            pullstr = "Merge #"

        commits = [
            (slug, comdate, msg)
            for slug, comdate, msg in commits
            if relstr not in msg]
        pulls = [
            (slug, msg)
            for slug, comdate, msg in commits
            if pullstr in msg]
        commits = [
            (slug, comdate, msg)
            for slug, comdate, msg in commits
            if pullstr not in msg]

        print
        print start
        print "-" * len(start)

        if pagure:
            pulls.extend(get_pull_request_pagure(project, commits[0]))

        if pulls:
            print
            print "Pull Requests"
            print

        if pagure:
            for number, title, author in pulls:
                author = "(@%s)" % author
                link = pull_url_for_pagure(project, number)

                print "- %s #%s, %s\n  %s" % (author.ljust(17), number, title, link)

        else:
            for slug, msg in pulls:
                number = msg[len(pullstr):].split()[0]
                try:
                    title, author, link = get_pull_info_github(
                        username, project, number)
                    author = "(@%s)" % author
                except KeyError as e:
                    sys.stderr.write('Problems getting info for '
                                     '#%s\n%r\n' % (number, e))
                    # Some fallbacks
                    author = ''
                    title = msg
                    link = pull_url_for_github(username, project, number)

                print "- %s #%s, %s\n  %s" % (author.ljust(17), number, title, link)

        if commits:
            print
            print "Commits"
            print

        for slug, comdate, msg in commits:
            if pagure:
                print "- %s %s\n  %s" % (
                    slug[:9], msg, commit_url_for_pagure(project, slug))
            else:
                print "- %s %s\n  %s" % (
                    slug[:9], msg,
                    commit_url_for_github(username, project, slug))


if __name__ == '__main__':
    args = parse_args()
    main(
        username=args.username,
        project=args.project,
        version=args.version,
        pagure=args.pagure,
    )
