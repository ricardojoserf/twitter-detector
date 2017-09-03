#!/bin/sh

cd /home/pi/Projects/twitter-detector && python main.py -q $1 -c $2 &
