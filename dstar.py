

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
			print "Data (str): " + data
		


