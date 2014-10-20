#!/bin/bash

if [ "$1" == "" ]; then
    key=$(zenity --entry --text="which password do you want?" --title="/usr/bin/pass")
else
    key=$1
fi

/usr/bin/pass -c $key

if [ $? -eq 0 ]; then
    notify-send "ok" "copied '$key'"
else
    notify-send -c error "uh oh" "something went wrong with '$key'"
fi
