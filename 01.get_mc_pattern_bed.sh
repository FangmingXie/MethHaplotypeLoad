#!/bin/bash

# given multiple regions (bed file), getting mc patterns for each read overlapping a given query region from bismark bam file
# This is a wrap up of the 01.1.get_mc_pattern.sh

# check parameters
if [[ -z "$1" ]]; then
    echo "Parameter 1 is empty"
    exit 1
elif [[ -z "$2" ]]; then
	echo "Parameter 2 is empty"
    exit 1
fi


# 0-based coords
bam=$1
bed=$2

# read through bed file
while read p || [ -n "$p" ]
do
	row=(${p//"\t"/" "})
	chr=${row[0]}
	start=${row[1]}
	end=${row[2]}
	01.1.get_mc_pattern.sh $bam $chr $((start+1)) $end
done < $bed

