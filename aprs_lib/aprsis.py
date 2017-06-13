import aprslib
import logging

import nmea
from util import config

def aprsis_dstar_callback(dstar_stream):
	# only send beacon from Kenwood D74
	if 'D74' in dstar_stream['sfx'] and '$GPGGA' in dstar_stream['gps']:
		cfg = config.config_load()
		# Connect to APRS-IS network if not already connected.
        	aprsIS = AprsIS(cfg.get("aprs-is", "callsign"), cfg.get("aprs-is", "password"))

		aprsIS.send_beacon(dstar_stream['my'], dstar_stream['sfx'], dstar_stream['message'], dstar_stream['gps']['$GPGGA'])

class AprsIS:

	logger = None
	instance = None
	
	class __AprsIS:
		def __init__(self, callsign, password):
			self.logger = logging.getLogger(__name__)
			self.aprs_connection = aprslib.IS(callsign, password)
			self.aprs_connection.connect()

	def __init__(self, callsign, password):
		if not AprsIS.instance:
			AprsIS.instance = AprsIS.__AprsIS(callsign, password)

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def send_beacon(self, callsign, sfx, message, gpgga):
		position = nmea.gpgga_get_position(gpgga)
		aprs_frame = callsign.strip()+'>APK'+sfx.strip()+',DSTAR*:!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a/A=' + position['height'] + message.strip()
		self.logger.info("Sending APRS Frame: " + aprs_frame)
		try:
			self.aprs_connection.sendall(aprs_frame)
			self.logger.info("APRS Beacon sent!")
		except Exception, e:
			self.logger.info("Invalid aprs frame [%s] - %s" % (aprs_frame, str(e)))
