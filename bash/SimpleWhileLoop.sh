#!/usr/bin/env bash

# METHOD 1
# Given number of retries
n=0
until [ $n -ge 3 ]
do
  wget -O - -q -t 1 http://localhost:8080/ && break
  n=$[$n+1]
  sleep 10
done

# METHOD 2
# Retries until it works
until docker ps
do
 sleep 3
done
