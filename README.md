# DStar Repeater Controller UDP Sniffer

This project tries to send every position received in a dstar repeater to aprs-is.

ICOM rpt sends all the traffic to the gateway using UDP port 20000.
We try to capture that traffic sniffing the network while we unserialize the udp packets to get
the slow speed data and routing information found in every DV transmission.

At the momento only kenwood /D74 received positions are sent to APRS-IS.

## Install
### We need pyaprs
```shell
pip install aprs
```
### Add file permissions
```shell
chmod a+x dstar_sniffer.py
```

### Run dstar_sniffer
```shell
./dstar_sniffer.py
```
#### or use this instead to leave it in background
```shell
nohup ./dstar_sniffer.py &
```

eliel (at) eliel.com.ar
