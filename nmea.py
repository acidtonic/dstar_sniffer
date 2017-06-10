def gpgga_get_position(gpgga_sentence):
	gps = re.search("\$GPGGA,,([0-9]+\.[0-9]+),([NS]),([0-9]+\.[0-9]+),([WE]),,,,([0-9]+),M,+\*(\w+)", gpgga_sentence)
	position = {}
	position['lat'] = gps.group(1)
	position['lat_coord'] = gps.group(2)
	position['long'] = gps.group(3)
	position['long_coord'] = gps.group(4)
	position['height'] = str(int(int(gps.group(5)) * 3.28084)).zfill(6)
	return position
