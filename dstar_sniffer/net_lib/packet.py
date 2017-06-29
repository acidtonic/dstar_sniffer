from struct import unpack
import socket

# Parses an IP packet, we only need UDP packets.
def parse_packet(packet, filter_ip, filter_port):
	#packet string from tuple
	packet = packet[0]

	#parse ethernet header
	eth_length = 14

	eth_header = packet[:eth_length]
	eth = unpack('!6s6sH' , eth_header)
	eth_protocol = socket.ntohs(eth[2])

	#Parse IP packets, IP Protocol number = 8
	if eth_protocol == 8 :
		# parse IP header
		ip_header = packet[eth_length:20+eth_length]
		iph = unpack('!BBHHHBBH4s4s' , ip_header)
		version_ihl = iph[0]
		version = version_ihl >> 4
		ihl = version_ihl & 0xF
		iph_length = ihl * 4
		protocol = iph[6]
		s_addr = socket.inet_ntoa(iph[8]);
		d_addr = socket.inet_ntoa(iph[9]);

		# UDP packets
		if protocol == 17 and (filter_ip == None or s_addr == filter_ip):
			u = iph_length + eth_length
			udph_length = 8
			udp_header = packet[u:u+8]
			udph = unpack('!HHHH' , udp_header)

			source_port = udph[0]
			dest_port = udph[1]
			length = udph[2]

			if (filter_port != None and dest_port != filter_port):
				return None

			h_size = eth_length + iph_length + udph_length
			data_size = len(packet) - h_size

			# get data from the packet
			data = packet[h_size:]
			return data
	return None
