
received_data = {}


def free_text(stream_data):
	txt = ""
	count = 0
	for c in stream_data:
		if (count % 6 == 0) and (c == '@' or (c >= 'A' and c <= 'Z')):
			for i in range(1, 5):
				count = count + 1
				txt = txt + c
		count = count + 1
	return txt

def parse_data(stream_data):
	print free_text(stream_data)

def parse_packet(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			# DV packet detected!
			if data_len == 58:
				print "DV INITIAL PACKET (routing info)"
				rpt2 = data[20:28]
				rpt1 = data[28:36]
				ur = data[36:44]
				my = data[44:52]
				sfx = data[52:56]

				print "START from rptr: cntr=%02x %02x, streamID=%d,%d, flags=%02x:%02x:%02x, my=%.8s, sfx=%.4s, ur=%.8s, rpt1=%.8s, rpt2=%.8s" % (packet[4], packet[5], packet[14], packet[15], packet[17], packet[18], packet[19], my, sfx, ur, rpt1, rpt2)
				received_data[packet[14] + packet[15]] = "" 
			elif data_len == 29 or data_len == 32:
				if packet[16] & 0x40:
					print "END OF STREAM %d,%d" % (packet[14], packet[15])
					print parse_data(received_data[packet[14] + packet[15]])

				else:
					if data_len == 32:
						received_data[packet[14] + packet[15]] = received_data[packet[14] + packet[15]] \
						+ chr(packet[29] ^ 0x70) + chr(packet[30] ^ 0x4F) + chr(packet[31] ^ 0x93)
					else:
						received_data[packet[14] + packet[15]] = received_data[packet[14] + packet[15]] \
						+ chr(packet[26] ^ 0x70) + chr(packet[27] ^ 0x4F) + chr(packet[28] ^ 0x93)


if __name__ == "__main__":
	with open('read_udp.data') as f:
		for line in f:
			if "hex" in line:
				line_hex = line.split(":")
				data = str(bytearray([int(x, 16) for x in line_hex[1:]]))
				parse_packet(data)
