import logging
import string

class DStar:

	stream = {}
	logger = None

	free_text_sequence = ['', '@', 'A', 'B', 'C']

	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def valid_nmea_sentence(self, sentence):
		try:
			if sentence[:3] == "$GP":
				to_verify = sentence[1:-3]
				crc = 0
				for i in range(0, len(to_verify)):
					crc = crc ^ ord(to_verify[i])
				if crc == int(sentence[-2:], 16):
					return True
			return False
		except ValueError:
			return False

	def valid_dprs_sentence(self, sentence):
		dprs = sentence.split(",", 1)[1]
		if dprs[-1:] != '\r':
			dprs = dprs + '\r'
		icomcrc = 0xffff
		for l in range(0, len(dprs)):
			ch = ord(dprs[l]) & 0xff
			for i in range(0, 8):
				xorflag = (((icomcrc ^ ch) & 0x01) == 0x01)
				icomcrc = (icomcrc >> 1) & 0x7fff
				if xorflag:
					icomcrc = icomcrc ^ 0x8408
				ch = (ch >> 1) & 0x7f
		return "$$CRC%04X" % ((~icomcrc) & 0xffff) == sentence.split(",", 1)[0]

	def valid_free_text_sequence(self, last_letter, current_letter):
		idx1 = self.free_text_sequence.index(last_letter)
		idx2 = self.free_text_sequence.index(current_letter)
		if (idx1 + 1 == idx2):
			return True
		return False

	def complete_missing_free_text_sequence(self, last_letter, current_letter):
		diff = self.free_text_sequence.index(current_letter) - self.free_text_sequence.index(last_letter)
		complete_string = ""
		for i in range(0, diff):
			complete_string = complete_string + "?????"
		return complete_string

	def free_text(self, stream_data):
		msg = ""
		last_letter = ''
		position = 0
		content = stream_data
		c = 0
		while c < len(content):
			if position % 6 == 0 and (content[c] == '@' or (content[c] >= 'A' and content[c] <= 'C')):
				if not self.valid_free_text_sequence(last_letter, content[c]):
					msg = msg + self.complete_missing_free_text_sequence(last_letter, content[c])
				last_letter = content[c]
				for i in range(0, 5):
					c = c + 1
					position = position + 1
					if content[c] in string.printable:
						msg = msg + content[c]
					else:
						msg = msg + '?'
				if self.free_text_sequence.index(last_letter) == len(self.free_text_sequence) - 1:
					# End of supported string sequence.
					break
			elif position % 6 == 0 and content[c] == '%':
				# 3 bytes syn sequence
				c = c + 3
				continue
			position = position + 1
			c = c + 1
		return msg

	def gps_info(self, stream_data):
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
				if self.valid_dprs_sentence(sentence):
					response["DPRS"] = sentence
				else:
					self.logger.info("Not valid DPRS sentence: " + sentence)
			if sentence.startswith('$GP'):
				# NMEA Sentence
				if self.valid_nmea_sentence(sentence):
					response[sentence.split(",")[0]] = sentence
				else:
					self.logger.info("Not valid NMEA sentence: " + sentence)
		return response

	def parse_data(self, stream_id):
		message = self.free_text(self.stream[stream_id]["slow_speed_data"])
		self.stream[stream_id]["message"] = message
		gps = self.gps_info(self.stream[stream_id]["slow_speed_data"])
		self.stream[stream_id]["gps"] = gps
		parsed_stream = self.stream[stream_id]
		del self.stream[stream_id]
		return parsed_stream 

	def scrambler(self, b1, b2, b3):
		return chr(b1 ^ 0x70) + chr(b2 ^ 0x4F) + chr(b3 ^ 0x93)

	def slow_speed_data(self, stream_id, new_data):
		self.stream[stream_id]["slow_speed_data"] = self.stream[stream_id]["slow_speed_data"] + new_data

	def parse(self, data):
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

					self.stream[stream_id] = {}
					self.stream[stream_id]["id"] = stream_id
					self.stream[stream_id]["my"] = my
					self.stream[stream_id]["sfx"] = sfx
					self.stream[stream_id]["ur"] = ur 
					self.stream[stream_id]["rpt1"] = rpt1
					self.stream[stream_id]["rpt2"] = rpt2
					self.stream[stream_id]["slow_speed_data"] = ""
					self.logger.info("Start of stream (%s) received from: %s" % (stream_id, my))
					return None
				elif data_len == 29 or data_len == 32:
					if packet[16] & 0x40:
						# end of stream!
						self.logger.info("End of stream (%s)" % stream_id)
						return self.parse_data(stream_id)
					else:
						# just another part of the stream
						self.slow_speed_data(stream_id, self.scrambler(packet[data_len-3], packet[data_len-2], packet[data_len-1]))
						return None

