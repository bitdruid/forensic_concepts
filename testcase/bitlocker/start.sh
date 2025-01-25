#!/bin/bash

/lib/systemd/systemd-udevd --daemon
udevadm trigger

echo "<<<<< Container initialized and running >>>>>"

exec tail -f /dev/null