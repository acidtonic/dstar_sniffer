

def parse(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			# DV packet detected!
			if data_len == 58:
				print "DV INITIAL PACKET (routing info)"
				rpt2 = data[20:8]
				rpt1 = data[28:8]
				ur = data[36:8]
				my = data[44:8]
				sfx = data[52:4]

				print "START from rptr: cntr=%02x %02x, streamID=%d,%d, flags=%02x:%02x:%02x, my=%.8s, sfx=%.4s, ur=%.8s, rpt1=%.8s, rpt2=%.8s" % (packet[4], packet[5], packet[14], packet[15], packet[17], packet[18], packet[19], my, sfx, ur, rpt1, rpt2)
			elif data_len == 29 or data_len == 32:
				if packet[16] & 0x40:
					print "END OF STREAM"
				else:
					print "DV VOICE+SLOW_DATA PACKET"
		


