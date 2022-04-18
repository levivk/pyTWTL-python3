#! /bin/bash
cd $(dirname $0)

# cd to script dir
cd $(dirname $0)

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ../pyTWTL/bin-linux/twtl_translate "[H^1 r2]^[0,10]" --kind=both
elif [[ "$OSTYPE" == "darwin"* ]]; then
    ../pyTWTL/bin-darwin/twtl_translate "[H^1 r2]^[0,10]" --kind=both
else
        echo "Unsupported OS type:" "$OSTYPE"
fi
