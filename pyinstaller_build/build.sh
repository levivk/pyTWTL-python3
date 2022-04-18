#!/bin/bash

# cd to script dir
cd $(dirname $0)

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	# Use docker to run in Ubuntu 18.04
	sudo docker build -t pytwtl .
	sudo docker create --name pytwtl-cont pytwtl
	rm -rf ../pyTWTL/bin-linux/*
	sudo docker cp pytwtl-cont:/b/dist/twtl_translate/. ../pyTWTL/bin-linux/
	sudo docker rm pytwtl-cont
	# change ownership
	sudo chown $(whoami):$(id -gn) -R ../pyTWTL/bin-linux/*

elif [[ "$OSTYPE" == "darwin"* ]]; then
	# remove dist and run pyinstaller
	rm -rf dist
	pyinstaller twtl_translate.spec
	# Copy to folder
	rm -rf ../pyTWTL/bin-darwin/*
    cp -ra dist/twtl_translate/. ../pyTWTL/bin-darwin/
else
        echo "Unsupported OS type:" "$OSTYPE"
fi
