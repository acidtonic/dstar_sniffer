import aprs
import nmea

class AprsIS:

	def __init__(self, callsign, password):
		self.aprs_connection = aprs.TCP(callsign, password)
		self.aprs_connection.start()

	def send_beacon(self, callsign, sfx, message, gpgga):
		position = nmea.gpgga_get_position(gpgga)
		print "Send beacon"
		aprs_frame = callsign+'>APK'+sfx+':!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a/A=' + position['height'] + '>' + message
		self.aprs_connection.send(aprs.Frame(aprs_frame))
