#!/usr/bin/env bash

n=0
until [ $n -ge 3 ]
do
  wget -O - -q -t 1 http://localhost:8080/ && break
  n=$[$n+1]
  sleep 10
done
