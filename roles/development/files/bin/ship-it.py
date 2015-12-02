#!/usr/bin/env python
""" Script for merging, pushing, building, updating, and buildroot-overriding
changes to a package.

Run this after you have made a change, committed and build the master branch.
"""

import argparse
import os
import sh
import sys
import six
import textwrap

import logging
logging.basicConfig(level=logging.DEBUG)

import fedmsg
import koji
build_state_names = {v: k for k, v in koji.BUILD_STATES.items()}

# sigh..
import time


aggregated = ""
passwd = ""

# open stdout in unbuffered mode
sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", 0)


def _handle_stdout(char, stdin):
    global aggregated
    global passwd

    if not isinstance(char, six.text_type):
        char = char.decode('utf-8')

    sys.stdout.write(char.encode('utf-8'))

    aggregated += char

    if "Password for ralph: " == aggregated:
        stdin.put(passwd + "\n")
        print "<entered>"
        aggregated = ""

    if char == "\n":
        aggregated = ""

io = dict(
    _out=_handle_stdout,
    _out_bufsize=0,
    _tty_in=True,
    #_tty_out=True,
    #_tty_in=True,
    #_in=sys.stdin,
    _err_to_out=True,
)

branches = [
    {
        'short': 'f23',
        'long': 'fc23',
    },
    {
        'short': 'f22',
        'long': 'fc22',
    },
    {
        'short': 'f21',
        'long': 'fc21',
    },
    {
        'short': 'f20',
        'long': 'fc20',
    },
    {
        'short': 'epel7',
        'long': 'el7',
    },
    {
        'short': 'el6',
        'long': 'el6',
    },
]


def config():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--user', dest='user',
        help='Your FAS username.')
    parser.add_argument(
        '--type', dest='type',
        help="Type.  (bugfix, enhancement, security)")
    parser.add_argument(
        '--bugs', dest='bugs', default=None,
        help="Specify any number of Bugzilla IDs (--bugs=1234,5678)")
    parser.add_argument(
        '--notes', dest='notes',
        help='Update notes')
    parser.add_argument(
        '--duration', dest='duration', type=int, default=7,
        help="Duration of the buildroot override in days.")
    parser.add_argument(
        '--branches', dest='branches', default='f19,f18',
        help="Duration of the buildroot override in days.")
    parser.add_argument(
        '--forgive-build', dest='forgive', action='store_true', default=False,
        help="Don't stop the script if a build fails.")
    parser.add_argument(
        '--skip-build', dest='skip', action='store_true', default=False,
        help="Don't build the package.")

    args = parser.parse_args()

    required_args = ['user', 'type', 'notes']
    for required in required_args:
        if not getattr(args, required):
            parser.print_usage()
            raise ValueError("%r is required." % required)

    return args


def main():
    bodhi_cmds = []
    args = config()
    spec = sh.glob("*.spec")[0]
    nevr = sh.rpmspec(q=spec).split()[0].rsplit('.', 2)[0]
    #passwd = getpass.getpass("Enter password:")
    print "Processing %r" % nevr
    branch_keys = args.branches.split(',')
    for branch_key in branch_keys:
        print "Handling %r" % branch_key
        branch = [b for b in branches if b['short'] == branch_key][0]
        nevra = nevr + '.' + branch['long']
        print "Working on %r, %r" % (branch['short'], nevra)
        p = sh.git.checkout(branch['short'], **io)
        p.wait()

        # Merge, push, build
        p = sh.git.merge("master", **io)
        p.wait()

        # This is ridiculous
        #p = sh.fedpkg.push(**io)
        #p.wait()
        os.system("git push --set-upstream origin " + branch['short'])
        time.sleep(0.5)

        if not args.skip:
            os.system("fedpkg build --nowait")

    nevras = []
    for branch_key in branch_keys:
        branch = [b for b in branches if b['short'] == branch_key][0]
        nevra = nevr + '.' + branch['long']
        nevras.append(nevra)

    print "Waiting for build results over fedmsg..."
    found = 0
    for n, e, topic, msg in fedmsg.tail_messages():
        if topic != 'org.fedoraproject.prod.buildsys.build.state.change':
            continue
        if msg['msg']['instance'] != 'primary':
            continue

        state = msg['msg']['new']
        state = build_state_names[state]

        nevra = "-".join([
            msg['msg']['name'],
            msg['msg']['version'],
            msg['msg']['release'],
        ])
        if nevra not in nevras:
            print "(ignoring)", nevra, state
            continue

        print nevra, state

        if state == 'BUILDING':
            continue

        for branch_key in branch_keys:
            branch = [b for b in branches if b['short'] == branch_key][0]
            if nevra.endswith(branch['long']):
                found += 1

        if found == len(branch_keys):
            break

    nevras = []
    for branch_key in branch_keys:
        branch = [b for b in branches if b['short'] == branch_key][0]
        nevra = nevr + '.' + branch['long']
        nevras.append(nevra)

    # For development...
    executable = os.path.expanduser(
        '~/.virtualenvs/bodhi-python2.7/bin/bodhi'
    )
    cmd = "%s updates new %s --user %s --type %s --notes \"%s\"" % (
        executable, ",".join(nevras), args.user, args.type, args.notes,
    )

    if args.bugs:
        cmd += " --bugs %s" % args.bugs

    print
    print "-" * 40
    print cmd
    # TODO -- actually submit the update via the python API instead..


if __name__ == '__main__':
    main()
