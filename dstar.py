
received_data = {}


def free_text(stream_data):
	txt = ""
	content = stream_data[3:]
	for c in range(0, len(content)):
		if (c % 6 == 0) and (content[c] == '@' or (content[c] >= 'A' and content[c] <= 'C')):
			for i in range(0, 5):
				c = c + 1
				txt = txt + content[c]
	return txt

def gps_info(stream_data):
	txt = ""
	content = stream_data[3:]
	for c in range(0, len(content)):
		if c % 6 == 0 and content[c] > 0x30 and content[c] <= 0x35:
			for i in range(0, content[c] - 0x30):
				c = c + 1
				txt = txt + content[c]
	return txt

def header(stream_data):
	txt = ""
	content = stream_data[3:]
	for c in range(0, len(content)):
		if c % 6 == 0 and content[c] > 0x50 and content[c] <= 0x55:
			for i in range(0, content[c] - 0x50):
				c = c + 1
				txt = txt + content[c]
	return txt

def parse_data(stream_data):
	print free_text(stream_data)
	print gps_info(stream_data)
	print header(stream_data)

def parse_packet(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			# DV packet detected!
			if data_len == 58:
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
					parse_data(received_data[packet[14] + packet[15]])

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
