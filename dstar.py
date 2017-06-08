

def parse(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			# DV packet
			print "DV PACKET!!!"

			if data_len == 58:
				my = ''.join(packet[44:8])
				sfx = ''.join(packet[52:4]
				ur = ''.join(packet[36:8])
				rpt1 = ''.join(packet[28:8])
				rpt2 = ''.join(packet[20:8])
	

				print "START from rptr: cntr=%02x %02x, streamID=%d,%d, flags=%02x:%02x:%02x, my=%.8s, sfx=%.4s, ur=%.8s, rpt1=%.8s, rpt2=%.8s" % (packet[4], packet[5], packet[14], packet[15], packet[17], packet[18], packet[19], my, sfx, ur, rpt1, rpt2)
		


