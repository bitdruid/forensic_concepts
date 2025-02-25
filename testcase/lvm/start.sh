#!/bin/bash

/lib/systemd/systemd-udevd --daemon
udevadm trigger

cd /app
testcase build

echo "<<<<< Container initialized and running >>>>>"

exec tail -f /dev/null