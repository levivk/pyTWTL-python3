#!/bin/bash

# cd to script dir
cd $(dirname $0)

# remove dist and run pyinstaller
rm -rf dist
pyinstaller twtl_translate.spec

# copy to respective folder
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        cp -r dist/twtl_translate ../pyTWTL/bin-linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
	rm -rf ../pyTWTL/bin-darwin
        cp -r dist/twtl_translate ../pyTWTL/bin-darwin
else
        echo "Unsupported OS type:" "$OSTYPE"
fi
