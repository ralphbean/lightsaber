My Ansible Setup
================

This is an ansible setup I use to manage my own machine(s).

I've tried to make it generic enough that you can clone it and use it too.

The playbooks in the ``playbooks/`` directory are separated out by user -- each
user keeps their own scripts there with no particular structure.  The
``roles/`` dir has shared roles, some of which do different things for
different users based on the presence of vars.  See
``roles/mail/client/tasks/main.yml`` for an example.


Credentials
-----------

I use `pass` to store the Ansible Vault password, which is used to
encrypt/decrypt the various passwords for each host in
``inventory/host_vars/hostname``.

You can generate the primary vault password by running `pass generate
sys/ansible/vault 32`. Then you can add something like `ansible_sudo_pass:
'foobar'` to `inventory/host_vars/127.0.0.1`.
