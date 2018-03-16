#!/bin/bash

# Find common users from all epoch files
i=0
tmp1="./tmp1$RANDOM"
tmp2="./tmp2$RANDOM"
tmp3="./tmp3$RANDOM"

for filename in ./userepochs*.csv; do
  if [ "$i" -eq 0 ];then
    awk '{print $1}' $filename | sort | uniq > $tmp1
  else
    awk '{print $1}' $filename | sort | uniq > $tmp2
    comm -12 $tmp1 $tmp2 > $tmp3
    mv $tmp3 $tmp1
  fi
  ((i++))
done

rm -f $tmp2
rm -f $tmp3
mv $tmp1 common_users.txt
sed -i '/device_id/d' common_users.txt
cat common_users.txt

# Generate daily files for common users
i=0
for filename in $(find . -maxdepth 1 -iname userepochs\* -type f | sort -V); do
  while read p; do
    # add header
    if [ "$i" -eq 0 ];then
     head -n 1 $filename > $p.txt
    fi
    # add days data
    grep $p $filename >> $p.txt
    sed -i -e "s/$p/day$((i+1))/g" $p.txt
  done < common_users.txt
  ((i++))
done

