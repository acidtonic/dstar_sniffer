

def parse_dstar(data):
	print "Data (hex): " + ":".join("{:02x}".format(ord(c)) for c in data)
	print "Data (str): " + data
