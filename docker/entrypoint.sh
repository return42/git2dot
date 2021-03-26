#!/bin/bash --login

set -e

PATH=/home/$USER/.local/bin:$PATH

exec "$@"
