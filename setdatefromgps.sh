#!/bin/sh
GPSDATE="`/usr/bin/gpspipe -w | /usr/bin/head -10 | /bin/grep TPV | /bin/sed -r 's/.*"time":"([^"]*)".*/\1/' | /usr/bin/head -1`"
/bin/date -s "$GPSDATE"
