#!/bin/sh
/usr/bin/sleep 10
GPSDATE="`/usr/bin/gpspipe -w | /usr/bin/head -10 | /bin/grep TPV | /bin/sed -r 's/.*"time":"([^"]*)".*/\1/' | /usr/bin/head -1`"
/usr/bin/sudo /bin/date -s "$GPSDATE"
/bin/date -s "$GPSDATE"
