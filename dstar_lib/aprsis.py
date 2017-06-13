import aprslib
import logging

import nmea

class AprsIS:

	logger = None

	def __init__(self, callsign, password):
		self.logger = logging.getLogger(__name__)
		self.aprs_connection = aprslib.IS(callsign, password)
		self.aprs_connection.connect()

	def send_beacon(self, callsign, sfx, message, gpgga):
		position = nmea.gpgga_get_position(gpgga)
		aprs_frame = callsign+'>APK'+sfx+',DSTAR*:!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a/A=' + position['height'] + message
		self.logger.info("Sending APRS Frame: " + aprs_frame)
		try:
			self.aprs_connection.sendall(aprs_frame)
			self.logger.info("APRS Beacon sent!")
		except Exception, e:
			self.logger.info("Invalid aprs frame [%s] - %s" % (aprs_frame, str(e))
