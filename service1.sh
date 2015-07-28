#!/bin/bash
#
# Working in App Containers
#   read|proces|write
#

usage(){
  program=`basename $0`
  echo "$program: Options --port --dip --dport --file"
  echo "$program: --port specifies the port service should use, default 6667"
  echo "$program: --dip specifiles the ip address where data goes to"
  echo "$program: --dport specifiles the tcp port where data goes to"
  echo "$program: --file specifiles the file name where data saved to"
}

ARGS=`getopt -l port:,dip:,dport:,file: -- -- "$@"`
#if [ $? -ne 0 ];then
#  usage
#  exit 1
#fi
eval set -- "${ARGS}"

# parse options
while true
do
  case "$1" in
    --port) 
        port=$2
        shift 2
        ;;
    --dip) 
        dip=$2
        shift 2
        ;;
    --dport) 
        dport=$2
        shift 2
        ;;
    --file) 
        file=$2
        shift 2
        ;;
    --)
        shift 
        break
        ;;
    *)
        echo "Internal error!"
        usage
        exit 1
        ;;
     esac
done

check_file(){
  file=$1
  [ ! -f $file ] && echo "creating $file" && touch $file
  [ ! -w $file ] && echo "$file not writable" && exit 1
}

# container's IP address
IP=`grep $HOSTNAME /etc/hosts|awk -F' ' '{print $1}'|tail -1`

# default port 6667 if port not specified
port=${port:=6667}

if [[ $file ]];then
    check_file
fi

if [[ $dip ]] && [[ $dport ]];then
  if [[ $file ]];then
    echo "redirecting to $dip $dport and $file"
      #nc -lk $IP $port | tr [:lower:] [:upper:] | tee -a $file | nc $dip $dport
      nc -l $IP $port | tr [:lower:] [:upper:] | tee -a $file | nc $dip $dport
  else
    echo "redirecting to $dip $dport"
      #nc -lk $IP $port | tr [:lower:] [:upper:] | nc $dip $dport
      nc -l $IP $port | tr [:lower:] [:upper:] | nc $dip $dport
  fi
else
  if [[ $file ]];then
    echo "redirecting to $file"
      #nc -lk $IP $port | tr [:lower:] [:upper:] | tee -a $file 
      nc -l $IP $port | tr [:lower:] [:upper:] | tee -a $file 
  else
    echo "no output specified"
  fi
fi
