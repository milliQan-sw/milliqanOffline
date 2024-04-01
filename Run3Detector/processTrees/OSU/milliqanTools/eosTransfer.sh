#!/usr/bin/bash

bash ~/accessEOS.sh

#rsync -zhv --stats --progress --ignore-existing /store/user/milliqan/run3/bar/1000/0000/*.root /eos/experiment/milliqan/run3/bar/1000/0000/

for i in {0..9}; do
  rsync -zh --ignore-existing --stats --progress /store/user/milliqan/run3/bar/1100/000${i}/*.root /eos/experiment/milliqan/run3/bar/1100/000${i}/;
done
