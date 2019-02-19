#!/bin/bash

# get current time
CURRENT=$(TZ='America/Los_Angeles' date "+%F %H:%M:%S")
CURRENT_HOUR=$(date +%H)

# get the next 3am
if [ $CURRENT_HOUR -lt 3 ] # it is already the same day
then
TARGET=$(TZ='America/Los_Angeles' date  "+%F 03:00:00")
else
TARGET=$(TZ='America/Los_Angeles' date -d "+1 days" "+%F 03:00:00")
fi

# get number of seconds between them
DIFF="$(($(date -d "$TARGET" '+%s') - $(date -d "$CURRENT" '+%s')))"

# call use_rgb.py and test_hardware.py with a timeout of that many seconds
timeout -s 2 $(($DIFF-1)) sudo python /home/group09/iot_ambilamp/code/test_hardware.py &
timeout -s 2 $(($DIFF-1)) sudo python /home/group09/iot_ambilamp/code/test_led.py &
