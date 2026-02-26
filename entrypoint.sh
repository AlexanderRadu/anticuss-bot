#!/bin/sh

if [ -z "$BOT_TOKEN" ]; then
    echo "====================================================================="
    echo "ERROR: The BOT_TOKEN environment variable is not set!"
    echo "Please specify it in the file.env or via startup parameters."
    echo "====================================================================="
    exit 1
fi

exec "$@"
