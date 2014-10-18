#!/usr/bin/python

# TODO finish docs
DOCUMENTATION = '''
---
module: gsettings
short_description: Set gsettings values.
# ... snip ...
'''

# TODO examples

# TODO with some arguments, should just get and return as a var
# TODO with no arguments should just list recurisvely and return as a var


import json
import shlex
import subprocess as sp
import sys

# read the argument string from the arguments file
args_file = sys.argv[1]
args_data = file(args_file).read()

args_lookup = {}
arguments = shlex.split(args_data)

for arg in arguments:
    if "=" not in arg:
        print json.dumps({
            "failed": True,
            "msg": "Argument %r is not of the form 'name=value'" % arg,
        })
        sys.exit(1)

    (key, value) = arg.split("=")
    args_lookup[key] = value

# Various arguments...
required = set(['schema', 'value', 'key'])
optional = set(['path'])
actual = set(args_lookup.keys())

missing = required - actual
if missing:
    print json.dumps({
        "failed": True,
        "msg": "Missing required fields %r" % missing,
    })
    sys.exit(1)

possible = required.union(optional)
extra = actual - possible
if extra:
    print json.dumps({
        "failed": True,
        "msg": "Extra fields found %r" % extra,
    })
    sys.exit(1)

value = args_lookup['value']
key = args_lookup['key']
schema = args_lookup['schema']
if 'path' in args_lookup:
    schema = schema + ":" + args_lookup['path']

# First, check to see if the field is even writable
cmd = [
    '/usr/bin/dbus-launch', '--exit-with-session', '/usr/bin/gsettings',
    'writable', schema, key,
]
proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
stdout, stderr = proc.communicate()
if proc.returncode != 0:
    print json.dumps({
        "failed" : True,
        "msg"    : "%r %r is not writable, %r, %r" % (schema, key, stdout, stderr),
    })
    sys.exit(proc.returncode)

# If it is writable, then see if it has the value we want
cmd = [
    '/usr/bin/dbus-launch', '--exit-with-session', '/usr/bin/gsettings',
    'get', schema, key,
]
proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
stdout, stderr = proc.communicate()
if stdout.strip().replace("', '", "','") in [value, "'%s'" % value]:
    print json.dumps({
        "changed": False,
    })
    sys.exit(0)

# If it has a different value, then write in the one we want.
cmd = [
    '/usr/bin/dbus-launch', '--exit-with-session', '/usr/bin/gsettings',
    'set', schema, key, value,
]
proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
stdout, stderr = proc.communicate()
if proc.returncode != 0:
    print json.dumps({
        "failed" : True,
        "msg"    : "failed to set %r %r to %r.\nstdout: %r\nstderr: %r\ncmd: %r" % (schema, key, value, stdout, stderr, cmd),
    })
    sys.exit(proc.returncode)

# Sometimes 'gsettings set' exits with code 0 even though it failed.
if 'dconf-WARNING' in stderr:
    print json.dumps({"failed" : True, "msg": stderr})
    sys.exit(1)

# Report that we are happy.
print json.dumps({
    "changed" : True
})
