import aprslib
import logging

import nmea
from passcode import passcode_generator
from ..util_lib import config

def to_aprs_callsign(dstar_callsign):
	module = dstar_callsign[-1:]
	return dstar_callsign[:-1].strip() + "-" + module

def aprsis_dstar_callback(dstar_stream):
	# only send beacon from Kenwood D74
	if 'D74' in dstar_stream['sfx'] and '$GPGGA' in dstar_stream['gps']:
		cfg = config.config_load()
		# Connect to APRS-IS network if not already connected for the specific rpt module.
		rpt_callsign = to_aprs_callsign(dstar_stream['rpt1'])
        	aprsIS = AprsIS(rpt_callsign)
		aprsIS.send_beacon(rpt_callsign, dstar_stream['my'], dstar_stream['sfx'], dstar_stream['message'], dstar_stream['gps']['$GPGGA'])

class AprsIS:

	logger = {}
	instance = {}
	aprs_connection = {}

	class __AprsIS:
		def __init__(self, callsign):
			self.logger[callsign] = logging.getLogger(__name__ + "-" + callsign)
			self.aprs_connection[callsign] = aprslib.IS(callsign, passcode_generator(callsign))
			self.aprs_connection[callsign].connect()

	def __init__(self, callsign):
		if callsign is not AprsIS.instance:
			AprsIS.instance[callsign] = AprsIS.__AprsIS(callsign)

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def send_beacon(self, rpt1, callsign, sfx, message, gpgga):
		position = nmea.gpgga_get_position(gpgga)
		aprs_frame = callsign.strip()+'>APK'+sfx.strip()+',DSTAR*:!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a/A=' + position['height'] + message.strip()
		self.logger.info("Sending APRS Frame: " + aprs_frame)
		try:
			self.aprs_connection[rpt1].sendall(aprs_frame)
			self.logger.info("APRS Beacon sent!")
		except Exception, e:
			self.logger.info("Invalid aprs frame [%s] - %s" % (aprs_frame, str(e)))

