#!/bin/bash

# bash generate random 32 character alphanumeric string (lowercase only)
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1

# bash generate random number between 0 and 9
cat /dev/urandom | tr -dc '0-9' | fold -w 256 | head -n 1 | head --bytes 1


