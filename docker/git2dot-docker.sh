#!/bin/bash

#set -x

# Launch git2dot inside docker

DOCKERIMAGE=local/git2dot

SCRIPTNAME="$(basename "$0")"
USAGE=`sed "s/__SCRIPTNAME__/$SCRIPTNAME/g" <<"EOF"
__SCRIPTNAME__ [-h] out/ repodir/

where:
    -h : show this help text
    out/ : directory into which dit and SVG files are to be saved
    repodir/ : Git repo to visualize
EOF
`

SIZEOPT=""
RANGE=""

seed=42
while getopts 'hs:r:' option; do
  case "$option" in
    h) echo "$USAGE"
       exit
       ;;
    # s) SIZEOPT="-s $OPTARG"
    #    ;;
    # r) RANGE="--slides $OPTARG"
    #    ;;
  esac
done
shift $((OPTIND - 1))

if [ $# -lt 2 ]; then
    echo "Error: I need 2 filenames" >&2
    echo >&2
    echo "$USAGE" >&2
    exit 1
fi

# Creating a directory for capturing the output
out=$1
mkdir -p $out

# Make sure we have an absolute path for the input
repo=`realpath $2`

# Temporary dir for container execution outputs
tempdir=`mktemp -d`

echo "Executing: docker run --rm -v $tempdir:/data/out -v $repo:/data/in $DOCKERIMAGE git2dot --verbose giant /data/out/results.svg /data/in"

docker run --rm -v $tempdir:/data/out -v $repo:/data/in $DOCKERIMAGE git2dot --verbose giant /data/out/results.svg /data/in | sed 's/^/   /'

if [ $? -ne 0 ]; then echo "Something wrong happened!" >&2 ; echo "results may be available in $tempdir."; exit 1; fi

echo "Done."

# Fetching results from the tempdir to the output dir
cp $tempdir/* $out/
rm -fr $tempdir

echo "Generated visualisation for $repo into $out"

