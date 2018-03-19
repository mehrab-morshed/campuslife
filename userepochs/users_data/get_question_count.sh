#!/bin/bash

# Generate daily files for common users
i=0
cat /dev/null > question_count.txt
for filename in $(find . -iname \*txt -type f); do
  echo $filename
  echo $(cut -d '.' -f2 <<< $filename)-$(($(awk '$7 != 0 {print $7}' $filename | wc -l)-1)) >> question_count.txt
done

