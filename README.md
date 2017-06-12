# DStar Repeater Controller UDP Sniffer

This project tries to send every position received in a dstar repeater to aprs-is.

ICOM rpt sends all the traffic to the gateway using UDP port 20000.
We try to capture that traffic sniffing the network while we unserialize the udp packets to get
the slow speed data and routing information found in every DV transmission.

At the momento only kenwood /D74 received positions are sent to APRS-IS.

## Useful links
- [Slow speed data] (http://www.qsl.net/kb9mwr/projects/dv/dstar/Slow%20Data.pdf)
- [UDP frames] (http://www.qsl.net/kb9mwr/projects/dv/dstar/formats%20of%20files%20and%20UDP-streams%20used%20on%20D-STAR.pdf)


eliel (at) eliel.com.ar
