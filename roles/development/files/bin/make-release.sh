#!/bin/bash

new_vers=$1
username=$2
project=$3
old_vers=$(grep version= setup.py | awk -F "'" {'print $2 '})

function warning() {
    echo "$*" >&2
}
function error() {
    echo "$*" >&2
    exit 1
}

function yesno() {
    local ans
    local ok=0
    local timeout=0
    local default
    local t

    while [[ "$1" ]]
    do
        case "$1" in
        --default)
            shift
            default=$1
            if [[ ! "$default" ]]; then error "Missing default value"; fi
            t=$(tr '[:upper:]' '[:lower:]' <<<$default)

            if [[ "$t" != 'y'  &&  "$t" != 'yes'  &&  "$t" != 'n'  &&  "$t" != 'no' ]]; then
                error "Illegal default answer: $default"
            fi
            default=$t
            shift
            ;;

        --timeout)
            shift
            timeout=$1
            if [[ ! "$timeout" ]]; then error "Missing timeout value"; fi
            if [[ ! "$timeout" =~ ^[0-9][0-9]*$ ]]; then error "Illegal timeout value: $timeout"; fi
            shift
            ;;

        -*)
            error "Unrecognized option: $1"
            ;;

        *)
            break
            ;;
        esac
    done

    if [[ $timeout -ne 0  &&  ! "$default" ]]; then
        error "Non-zero timeout requires a default answer"
    fi

    if [[ ! "$*" ]]; then error "Missing question"; fi

    while [[ $ok -eq 0 ]]
    do
        if [[ $timeout -ne 0 ]]; then
            if ! read -t $timeout -p "$*" ans; then
                ans=$default
            else
                # Turn off timeout if answer entered.
                timeout=0
                if [[ ! "$ans" ]]; then ans=$default; fi
            fi
        else
            read -p "$*" ans
            if [[ ! "$ans" ]]; then
                ans=$default
            else
                ans=$(tr '[:upper:]' '[:lower:]' <<<$ans)
            fi 
        fi

        if [[ "$ans" == 'y'  ||  "$ans" == 'yes'  ||  "$ans" == 'n'  ||  "$ans" == 'no' ]]; then
            ok=1
        fi

        if [[ $ok -eq 0 ]]; then warning "Valid answers are: yes y no n"; fi
    done
    [[ "$ans" = "y" || "$ans" == "yes" ]]
}


if [ -z $new_vers ] ; then
    echo "No 'new version' specified.";
    echo "usage: make-release.sh NEW_VERSION GITHUB_ORGANIZATION PROJECT_NAME"
    exit 1;
fi

if [ -z $old_vers ] ; then
    old_vers=$(grep "version =" setup.py | awk -F "'" {'print $2 '})
    if [ -z $old_vers ] ; then
        echo "FAIL:  Couldn't figure out 'old version'.";
        exit 1;
    fi
fi

if [ -z $username ] ; then
    echo "No 'username' specified.";
    echo "usage: make-release.sh NEW_VERSION GITHUB_ORGANIZATION PROJECT_NAME"
    exit 1;
fi

if [ -z $project ] ; then
    echo "No 'project' specified.";
    echo "usage: make-release.sh NEW_VERSION GITHUB_ORGANIZATION PROJECT_NAME"
    exit 1;
fi

echo "Cutting release '$new_vers' from '$old_vers' (for $username/$project)"
if yesno "Is this correct?"; then
    git flow release start $new_vers
    make-changelog.py --username $username --project $project --version $new_vers > CHANGELOG.rst
    sed -i "s/$old_vers/$new_vers/g" setup.py
    git add CHANGELOG.rst setup.py
    git commit -m $new_vers
    if yesno "Do you want to shoot this off to PyPI?"; then
        if [ -f Makefile ]; then
            make upload
        else
            python setup.py sdist upload --sign
        fi
    fi
    git flow release finish -m $new_vers -u 971095FF $new_vers
else
    echo Okay.. bailing.
    exit 1
fi

if yesno "Do you want to push the release back to github?"; then
    flow-finish.sh
fi

if yesno "Do you want to force a version check with anitya?"; then
    check-anitya.py $project
fi

echo
echo "Fedora Stuff"
echo "------------"

letter=$(echo $project | cut -b 1)
url=https://pypi.python.org/packages/source/$letter/$project/$project-$new_vers.tar.gz
echo "To start along with .spec packaging, you'll want to run:"
echo "$ cd \$FEDPKG_DIR"
echo "$ freshness"
echo "$ wget $url"
echo "$ fedpkg new-sources $project-$new_vers.tar.gz"
echo "$ rpmdev-bumpspec -n $new_vers *.spec"
echo "$ git commit -a -m '$new_vers'"
echo "$ fedpkg push && fedpkg build --nowait"

