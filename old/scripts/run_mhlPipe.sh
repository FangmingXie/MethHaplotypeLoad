#!/bin/bash
# for loop
for file in cfg_*
do
	nohup ./mhl_code/mhlPipe.py $file > $file.log 2>&1 &
done