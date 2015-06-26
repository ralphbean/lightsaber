#!/bin/bash -xv

dest=/run/media/threebean/14ec7ae9-a7f6-4702-92fd-146b6ed2b074

for item in password-store gnupg ssh task; do
    #cp -rvf ~/.${item} ${dest}/${item}
    rsync -avzh --progress ~/.${item}/ ${dest}/${item}
done
