import aprs
import nmea

class AprsIS:

	def __init__(self, callsign, password):
		self.aprs_connection = aprs.TCP(callsign, password)
		self.aprs_connection.start()

	def send_beacon(self, callsign, sfx, message, gpgga_sentence):
		position = nmea.gpgga_get_position(gpgga_sentence)
		print "Send beacon"
		aprs_frame = callsign+'>APK'+sfx+':!'+gpgga['lat'] + gpgga['lat_coord'] + '/'+gpgga['long']+gpgga['long_coord']+'Da/A=' + gpgga['height'] + '>' + message
		self.aprs_connection.send(aprs.Frame(aprs_frame))
