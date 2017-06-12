# DStar Repeater Controller UDP Sniffer

This project tries to send every position received in a dstar repeater to aprs-is.

ICOM rpt sends all the traffic to the gateway using UDP port 20000.
We try to capture that traffic sniffing the network while we unserialize the udp packets to get
the slow speed data and routing information found in every DV transmission.

At the momento only kenwood /D74 received positions are sent to APRS-IS.

## Install
### Install dstar_sniffer
```shell
python setup.py install
```
All the configuration files will be installed in /etc/dstar_sniffer/

### Run dstar_sniffer
```shell
dstar_sniffer
```
#### or use this instead to leave it in background
```shell
nohup ./dstar_sniffer.py &
```
### Logging
Dstar Sniffer will log all its output to /var/log/dstar_sniffer.log

eliel (at) eliel.com.ar
