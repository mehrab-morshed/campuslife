#!/bin/bash

i=0

declare -A usermap
for filename in $(find . -iname userepochs\* -type f | sort -V); do
  for user in $(awk '{print $1}' $filename | sort | uniq | grep -v device_id); do
    if [ ${usermap[$user]+abc} ]; then
      ((usermap[$user]++))
    else
      usermap[$user]=1
    fi
  done
done

# print users with data for atleast 5 days
numdays=5
cat /dev/null > users_with_atleast_${numdays}_days_of_data.txt
for user in "${!usermap[@]}"; do
  if [ ${usermap[$user]} -ge $numdays ]; then
    echo $user-${usermap[$user]} >> users_with_atleast_${numdays}_days_of_data.txt
  fi
done



