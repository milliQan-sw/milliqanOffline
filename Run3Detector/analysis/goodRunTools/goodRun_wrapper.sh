#!/usr/bin/bash

source ~/root_condor.sh
echo "Running on computer $(hostname)"

tar -xzf configurations.tar.gz

if [ "$#" -gt 2 ]; then

  echo "Running on Directories: $2 $3"

  python3 checkMatching.py -d $2 -s $3 -c configuration/barConfigs/
  
  mv *.json $4

else

 # Check if the user provided an argument
  if [ $# -eq 0 ]; then
    echo "Usage: $0 <number>"
    exit 1
  fi

  # Number to search for
  search_number=$(( $1 + 1 ))

  # File path
  file_path="directoryList.txt"

  line=$(sed -n "${search_number}p" "$file_path")

  # Extract the two numbers from the line and set them as variables
  read first_num second_num <<< "$line"

  # Print the values of the variables
  echo "Running on Directories: $first_num $second_num" 

  python3 checkMatching.py -d $first_num -s $second_num -c configuration/barConfigs/

  mv *.json $2

fi

