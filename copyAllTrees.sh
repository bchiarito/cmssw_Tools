#! /bin/bash

echo $1
for i in $1/*
do
  echo $i
  root -l -q $i copytree.C &
done
