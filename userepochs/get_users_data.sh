#!/bin/bash

# Generate daily files for common users
i=0
for filename in $(find . -iname userepochs\* -type f | sort -V); do
  daylabel=$(awk -F '[-./]' '{print $5}' <<< ${filename})
  echo $filename-$daylabel
  while read p; do
    # add header
    if [ "$i" -eq 0 ];then
      head -n 1 $filename > $p.txt
    fi
    # add days data
    grep $p $filename >> $p.txt
    sed -i -e "s/$p/$daylabel/g" $p.txt
  done < users_with_atleast_5_days_of_data_withoutcount.txt
  ((i++))
done

