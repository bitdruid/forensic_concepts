#!bin/bash

cd /app
testcase build

echo "<<<<< Container initialized and running >>>>>"

exec tail -f /dev/null