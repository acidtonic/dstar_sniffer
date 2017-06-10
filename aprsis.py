import aprs
import nmea

class AprsIS:

	def __init__(self, callsign, password):
		self.aprs_connection = aprs.TCP(callsign, password)
		self.aprs_connection.start()

	def send_beacon(self, callsign, message, gpgga_sentence):
		position = nmea.gpgga_get_position(gpgga_sentence)
		print "Send beacon"
		#self.aprs_connection.send()
