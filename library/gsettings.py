#!/usr/bin/python
# Copyright (C) 2017 Red Hat, Inc.
#
# This ansible gsettings module is free software; you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the License,
# or (at your option) any later version.
#
# This ansible gsettings module is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this ansible gsettings module; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Ralph Bean <rbean@redhat.com>

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


def main():
    module = AnsibleModule(
        argument_spec = dict(
            schema = dict(required=True),
            value = dict(required=True),
            key = dict(required=True),
            path = dict(required=False, default=None),
        ),
    )

    schema = module.params['schema']
    key = module.params['key']
    value = module.params['value']
    path = module.params['path']
    if path is not None:
        schema = '%s:%s' % (schema, path)

    dbus_bin = module.get_bin_path('dbus-launch', required=True)
    gsettings_bin = module.get_bin_path('gsettings', required=True)
    # First, check to see if the field is even writable
    cmd = [
        dbus_bin, '--exit-with-session', gsettings_bin,
        'writable', schema, key,
    ]
    (rc, stdout, stderr) = module.run_command(cmd)
    if rc != 0:
        module.fail_json(msg="%r %r is not writable, %r, %r" % (schema, key, stdout, stderr))

    # If it is writable, then see if it has the value we want
    cmd = [
        dbus_bin, '--exit-with-session', gsettings_bin,
        'get', schema, key,
    ]
    (rc, stdout, stderr) = module.run_command(cmd)

    if stdout.strip().replace("', '", "','") in [value, "'%s'" % value]:
        module.exit_json(changed=False)

    # If it has a different value, then write in the one we want.
    cmd = [
        dbus_bin, '--exit-with-session', gsettings_bin,
        'set', schema, key, value,
    ]
    (rc, stdout, stderr) = module.run_command(cmd)
    if rc != 0:
        module.fail_json(msg="failed to set %r %r to %r.\nstdout: %r\nstderr: %r\ncmd: %r" % (schema, key, value, stdout, stderr, cmd))

    # Sometimes 'gsettings set' exits with code 0 even though it failed.
    if 'dconf-WARNING' in stderr:
        module.fail_json(msg=stderr)

    # Report that we are happy.
    module.exit_json(changed=True)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
