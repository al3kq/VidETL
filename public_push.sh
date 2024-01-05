#!/bin/sh

echo "You are about to push to the public repository."
echo "Are you sure? (y/n)"
read answer < /dev/tty

if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
    echo "Push aborted."
    exit 1
fi

exit 0
