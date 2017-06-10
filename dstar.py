received_data = {}

stream = {}

def valid_nmea_sentence(sentence):
	try:
		if sentence[:3] == "$GP":
			to_verify = sentence[1:-3]
			crc = 0
			for i in range(0, len(to_verify)):
				crc = crc ^ ord(to_verify[i])
			if crc == int(sentence[-2:], 16):
				return 1
		return 0
	except ValueError:
		return 0

def valid_dprs_sentence(sentence):
	icomcrc = 0xffff
	for l in range(0, len(sentence)):
		ch = ord(sentence[l]) & 0xff
		for i in range(0, 8):
			xorflag = ((icomcrc ^ ch) & 0x01) == 0x01
			icomcrc = icomcrc >> 1
			if xorflag:
				icomcrc = icomcrc ^ 0x8408
			ch = ch >> 1
	return hex((~icomcrc) & 0xffff)

def free_text(stream_data):
	msg = ""
	content = stream_data[3:]
	for c in range(0, len(content)):
		if (c % 6 == 0) and (content[c] == '@' or (content[c] >= 'A' and content[c] <= 'C')):
			for i in range(0, 5):
				c = c + 1
				msg = msg + content[c]
	return msg

def gps_info(stream_data):
	gps_sentence = ""
	content = stream_data[3:]
	position = 0
	c = 0
	while c < len(content):
		if position % 6 == 0 and content[c] == '%':
			# 3 bytes sync sequence
			c = c + 3 
			continue
		elif position % 6 == 0 and ord(content[c]) > 0x30 and ord(content[c]) <= 0x35:
			stream_length = ord(content[c]) - 0x30
			for i in range(0, stream_length):
				position = position + 1
				c = c + 1
				gps_sentence = gps_sentence + content[c]
		position = position + 1
		c = c + 1
	response = {}
	for sentence in gps_sentence.split('\n'):
		sentence = sentence.strip()
		if sentence.startswith('$$CRC'):
			# DPR-S Sentence
			if valid_dprs_sentence(sentence):
				response["DPRS"] = sentence
			else:
				print "Not valid DPRS sentence: " + sentence
		if sentence.startswith('$GP'):
			if sentence.endswith('\r'):
				print "sentence: %s termina con r" % sentence
			# NMEA Sentence
			if valid_nmea_sentence(sentence):
				response[sentence.split(",")[0]] = sentence
			else:
				print "Not valid NMEA sentence: " + sentence
	return response

def parse_data(stream_id):
	message = free_text(stream[stream_id]["slow_speed_data"])
	stream[stream_id]["message"] = message
	gps = gps_info(stream[stream_id]["slow_speed_data"])
	stream[stream_id]["gps"] = gps
	print stream[stream_id]

def scrambler(b1, b2, b3):
	return chr(b1 ^ 0x70) + chr(b2 ^ 0x4F) + chr(b3 ^ 0x93)

def slow_speed_data(stream_id, new_data):
	stream[stream_id]["slow_speed_data"] = stream[stream_id]["slow_speed_data"] + new_data

def parse_packet(data):
	if data.startswith("DSTR", 0, 4):
		data_len = len(data)

		packet = list(bytearray(data))

		if (data_len == 58 or data_len == 29 or data_len == 32) and packet[6] == 0x73 \
		and packet[7] == 0x12 and packet[10] == 0x20 and packet[8] == 0x00 and \
		(packet[9] == 0x30 or packet[9] == 0x13 or packet[9] == 0x16):
			stream_id = packet[14] + packet[15]

			# DV packet detected!
			if data_len == 58:
				# start of stream
				rpt2 = data[20:28]
				rpt1 = data[28:36]
				ur = data[36:44]
				my = data[44:52]
				sfx = data[52:56]

				stream[stream_id] = {}
				stream[stream_id]["my"] = my
				stream[stream_id]["sfx"] = sfx
				stream[stream_id]["ur"] = ur 
				stream[stream_id]["rpt1"] = rpt1
				stream[stream_id]["rpt2"] = rpt2
				stream[stream_id]["slow_speed_data"] = ""
			elif data_len == 29 or data_len == 32:
				if packet[16] & 0x40:
					# end of stream!
					parse_data(stream_id)
				else:
					# just another part of the stream
					slow_speed_data(stream_id, scrambler(packet[data_len-3], packet[data_len-2], packet[data_len-1]))

