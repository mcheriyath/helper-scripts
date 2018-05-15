#!/bin/bash

## Make sure you copy your SSH key before you run this script
## ssh-copy-id -i ~/.ssh/id_rsa.pub <ServerIP>

IPS=`cat /tmp/dc1.txt`
for IP in $IPS
do
    DOMAINNAME=$(dig -x $IP +short)
    CPU=$(ssh $IP nproc)
    MEM=$(ssh $IP free -m | grep Mem | awk '{print $2}')
    DISK=$(ssh $IP df -h | awk '$NF=="/"{printf "%dGB \n", $2}')
    echo "$DOMAINNAME, $CPU, $MEM, $DISK" >> DC1-FreeMachines.txt
done


IPPS=`cat /tmp/dc2.txt`
for IPP in $IPPS
do
     DOMAINNAME=$(dig -x $IPP +short)
     CPU=$(ssh $IPP nproc)
     MEM=$(ssh $IPP free -m | grep Mem | awk '{print $2}')
     DISK=$(ssh $IPP df -h | awk '$NF=="/"{printf "%dGB \n", $2}')
     echo "$DOMAINNAME, $CPU, $MEM, $DISK" >> DC2-FreeMachines.txt
done

#IPS=`cat /tmp/dc1.txt`
#for IP in $IPS
#do
#     DOMAINNAME=$(dig -x $IP +short | awk '{printf "DomainName: %s \n",$1}')
#     CPU=$(ssh $IP nproc | awk '{printf "CPU Cores: %s \n",$1 }')
#     MEM=$(ssh $IP free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
#     DISK=$(ssh $IP df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}')
#     echo "$DOMAINNAME, $CPU, $MEM, $DISK" >> DC1-FreeMachines.txt
#done


#IPPS=`cat /tmp/dc2.txt`
#for IPP in $IPPS
#do
#      DOMAINNAME=$(dig -x $IPP +short | awk '{printf "DomainName: %s \n",$1}')
#      CPU=$(ssh $IPP nproc | awk '{printf "CPU Cores: %s \n",$1 }')
#      MEM=$(ssh $IPP free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
#      DISK=$(ssh $IPP df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}')
#      echo "$DOMAINNAME, $CPU, $MEM, $DISK" >> DC2-FreeMachines.txt
#done
