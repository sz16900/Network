# This script is to demonstrate that a two way connecting is needed in
# order to have an only https/443 firewall setup.

import sys, os, subprocess as sp

def allow_443_incoming(DEBUG=False):
    options = {'iptables': '/sbin/iptables', 'protocol': 'tcp', 'port': 443}
    ipcommands = '{iptables} -A INPUT -p {protocol} --dport {port} -m conntrack --ctstate \
    NEW,ESTABLISHED -j ACCEPT'.format(**options)

    if DEBUG:
        print ipcommands
    else:
		sp.call('/sbin/iptables -F', shell=True)
		sp.call(ipcommands, shell=True)
		sp.call('/sbin/iptables -A INPUT -m conntrack -j ACCEPT  --ctstate RELATED,ESTABLISHED', shell=True)
		sp.call('/sbin/iptables -A INPUT -j DROP', shell=True)
		sp.call('/sbin/iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT', shell=True)
		sp.call('/sbin/iptables -A FORWARD -j DROP', shell=True)

if __name__ == '__main__':
    # Check if you are running as root
    if os.getuid() != 0:
        print "You must be root to create policies with iptables."
        sys.exit(2)
    else:
        allow_443_incoming()
