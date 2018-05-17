#/bin/bash
filename=$1
program=$2
while :
do
  if [ -e $filename ]
  then
    rm -rf $filename
    python $program
  fi
done
