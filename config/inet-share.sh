#!/bin/bash

set -o nounset
set -o errexit

print_usage_string () {
    echo -n "Usage: inet-share.sh [OPTIONS]
Forward connections from one interface to another

  -u, --unshare     Undo connection forwarding
  -f, --from        Source interface (default wlp9s0)
  -t, --to          Target interface (default enp8s0)
  -h, --help        display this help and exit
"
}

TEMP=$( getopt -o u,f:,t:,h -l unshare,from:,to:,help \
    -n 'inet-share.sh' -- "$@" )

eval set -- "$TEMP"
while true ; do
    case $1 in
        -u|--unshare)
            iptable_action=-D ; shift 1 ;;
        -f|--from)
            from_iface=$2 ; shift 2 ;;
        -t|--to)
            to_iface=$2 ; shift 2 ;;
        -h|--help)
            print_usage_string ; exit 0 ; shift 1;;
        --) shift 1 ; break ;;
        *) echo "Invalid argument: $1" ; print_usage_string ; exit 1 ;;
    esac
done

VERBOSE=${VERBOSE:-0}
iptable_action=${iptable_action:--A}
from_iface=${from_iface:-wlp9s0}
to_iface=${to_iface:-enp8s0}

if [[ "$iptable_action" = "-A" ]]; then
    sysctl net.ipv4.ip_forward=1
else
    sysctl net.ipv4.ip_forward=0
fi

(( VERBOSE )) && _echo () { echo $@ >&2 ; } || _echo () { :; }
(( VERBOSE )) && _errorstream () { cat - >&2 ; } || _errorstream () { :; }

iptables -t nat ${iptable_action} POSTROUTING -o ${from_iface} -j MASQUERADE
iptables ${iptable_action} FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables ${iptable_action} FORWARD -i ${to_iface} -o ${from_iface} -j ACCEPT
