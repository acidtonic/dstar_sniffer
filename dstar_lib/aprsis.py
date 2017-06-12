import aprs

import nmea

class AprsIS:

	logger = None

	def __init__(self, logger, callsign, password):
		self.logger = logger
		self.aprs_connection = aprs.TCP(callsign, password)
		self.aprs_connection.start()

	def send_beacon(self, callsign, sfx, message, gpgga):
		position = nmea.gpgga_get_position(gpgga)
		aprs_frame = callsign+'>APK'+sfx+',DSTAR*:!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a/A=' + position['height'] + message
		self.logger.info("Sending APRS Frame: " + aprs_frame)
		try:
			self.aprs_connection.send(aprs.Frame(aprs_frame))
		except:
			self.logger.info("Invalid aprs frame: " + aprs_frame)
