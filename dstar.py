

def parse(data):
	if data.startswith("DSTR", 0, 4):
		print "Data (hex): " + ":".join("{:02x}".format(ord(c)) for c in data)
		print "Data (str): " + data
		
		data_len = len(data)

		print data_len + " [0] = " + data[0]

		if (data_len == 58 or data_len == 29 or data_len == 32) and data[6] == 0x73 \
		and data[7] == 0x12 and data[10] == 0x20 and data[8] == 0x00 and \
		(data[9] == 0x30 or data[9] == 0x13 or data[9] == 0x16):
			# DV packet
			print "DV PACKET!!!"


