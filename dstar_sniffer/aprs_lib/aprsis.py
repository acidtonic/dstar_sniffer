import aprslib
import logging

import nmea
from passcode import passcode_generator

def to_aprs_callsign(dstar_callsign):
	module = dstar_callsign[-1:]
	return dstar_callsign[:-1].strip() + "-" + module

def aprsis_dstar_callback(dstar_stream):
	logger =  logging.getLogger(__name__)

	if '$GPGGA' in dstar_stream['gps']:
		# detect kenwood HTs and send aprs beacons.
		# Connect to APRS-IS network if not already connected for the specific rpt module.
		frame = get_beacon_gpgga(dstar_stream['my'], dstar_stream['sfx'], dstar_stream['message'], dstar_stream['gps']['$GPGGA'])
	elif 'DPRS' in dstar_stream['gps']:
		#detect ICOM GPS-A dprs format and send aprs beacon
		frame = get_beacon_dprs(dstar_stream['gps']['DPRS'])
	else:
		logger.info("Nothing to do with: %s /%s" % (dstar_stream['my'], dstar_stream['sfx']))
		return
	rpt_callsign = to_aprs_callsign(dstar_stream['rpt1'])
	logger.info("Sending frame: %s" % frame)
	aprs = aprslib.IS(rpt_callsign, passcode_generator(rpt_callsign))
	aprs.connect()
	aprs.sendall(frame)
	aprs.close()


def get_beacon_dprs(dprs_sentence):
	aprs_frame = dprs_sentence.split(",", 1)[1]
	return aprs_frame

def get_beacon_gpgga(callsign, sfx, message, gpgga):
	position = nmea.gpgga_get_position(gpgga)
	height = ''
	if 'height' in position:
		height = '/A=' + position['height']
	aprs_frame = callsign.strip()+'>APK'+sfx.strip()+',DSTAR*:!'+position['lat'] + position['lat_coord'] + '\\'+position['long']+position['long_coord']+'a' + height + message.strip()
	return aprs_frame
