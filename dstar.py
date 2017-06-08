

def parse(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			# DV packet
			print "DV PACKET!!!"
			print "Data (hex): " + ":".join("{:02x}".format(ord(c)) for c in data)
			print "START from rptr: cntr=%02x %02x, streamID=%d,%d, flags=%02x:%02x:%02x, my=%.8s, sfx=%.4s, ur=%.8s, rpt1=%.8s, rpt2=%.8s" % (pkt[4], pkt[5], pkt[14], pkt[15], pkt[17], pkt[18], pkt[19], pkt[44], pkt[52], pkt[36], pkt[28], pkt[20])
		


