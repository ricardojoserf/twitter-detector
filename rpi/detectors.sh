#!/bin/sh

cd /home/pi/Projects/twitter-detector && python tweets.py -q $1 -c $2 &
