# DStar Repeater Controller UDP Sniffer

This project tries to send every position received in a dstar repeater to aprs-is.

ICOM rpt sends all the traffic to the gateway using UDP port 20000.
We try to capture that traffic sniffing the network while we unserialize the udp packets to get
the slow speed data and routing information found in every DV transmission.

At the moment only kenwood /D74 received positions are sent to APRS-IS.

## Install
### Install dstar_sniffer
```shell
python setup.py install
```
All the configuration files will be installed in /etc/dstar_sniffer/

### Run dstar_sniffer
```shell
usage: dstar_sniffer [start|stop|restart]
```

```shell
dstar_sniffer start
```
### Logging
Dstar Sniffer will log all its output to /var/log/dstar_sniffer.log
If you want to modify this you need to edit the /etc/dstar_sniffer/logging.conf file.

### Configuration file (/etc/dstar_sniffer/dstar_sniffer.conf)
```
[controller]
port= <where the icom rpt controller sends all the DV traffic>
iface= <name of the interface where the icom rpt controller is connected to the gateway>
ip= <ip of the icom rpt controller>
```

eliel (at) eliel.com.ar
