#!/bin/bash
destdir=/var/backups/stats/
hosts=("10.7.0.7","10.7.0.6","10.7.0.5","10.8.0.1","10.8.0.97")
key=/var/backups/.ssh/backup

for host in "${hosts[@]}"
do
    rsync -e "ssh -i $key" -avP --remove-source-files --ignore-existing "backup@$host:stats.csv" $destdir
done

