---===DStar Repeater Controller UDP Sniffer ===---

This project will try to send every position received in a dstar repeater to aprs-is.

ICOM rpt sends all the traffic to the gateway using UDP port 20000.
We try to capture that traffic sniffing the network while we unserialize the udp packets to get
the slow data and routing information found in every DV transmission.

This project is not in alpha stage yet :( we are working every day to get it done as soon as possible.

eliel at eliel.com.ar
