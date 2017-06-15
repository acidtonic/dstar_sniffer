from datetime import datetime
import time

from last_heard_render import render_last_heard_html
from dstar_sniffer.util_lib import config
from dstar_sniffer.aprs_lib.nmea import gpgga_get_position

def last_heard_callback(dstar_stream):
	last = LastHeard()
	last.add(dstar_stream)

class LastHeard:

	instance = None

	class __LastHeard:

		last_heard = {}
		output_html_file = None
		
		def __init__(self):
			cfg = config.config_load()
			self.output_html_file = cfg.get("last_heard", "output_file")

	def __init__(self):
		if LastHeard.instance == None:
			LastHeard.instance = LastHeard.__LastHeard()

        def __getattr__(self, name):
                return getattr(self.instance, name)

	def add(self, dstar_stream):
		cs_user = dstar_stream['my'].strip()

		if cs_user in self.last_heard:
			del self.last_heard[cs_user]
		self.last_heard[cs_user] = {}

		self.last_heard[cs_user]['time'] = datetime.now()
		self.last_heard[cs_user]['ur'] = dstar_stream['ur']
		self.last_heard[cs_user]['my'] = dstar_stream['my']
		self.last_heard[cs_user]['sfx'] = dstar_stream['sfx']
		self.last_heard[cs_user]['rpt1'] = dstar_stream['rpt1']
		self.last_heard[cs_user]['rpt2'] = dstar_stream['rpt2']
		self.last_heard[cs_user]['message'] = dstar_stream['message']
		self.last_heard[cs_user]['gps'] = dstar_stream['gps']
		self.last_heard[cs_user]['raw'] = dstar_stream['slow_speed_data']
		if '$GPGGA' in dstar_stream['gps']:
			position = gpgga_get_position(dstar_stream['gps']['$GPGGA'])
			lat_sign = ''
			long_coord = ''
			if position['lat_coord'] == 'S':
				lat_sign = '-'
			if position['long_coord'] == 'W':
				long_sign = '-'
			self.last_heard[cs_user]['latitude'] = lat_sign + self.gpgga_latitude_to_gmap(position['lat'])
			self.last_heard[cs_user]['longitude'] = long_sign + self.gpgga_longitude_to_gmap(position['long'])
		# remove old entries.
		self.cleanup()
		self.update_output()

	def gpgga_latitude_to_gmap(self, value):
		position = str(value)
		return str(float(float(position[:2]) + float(position[2:]) / 60))

	def gpgga_longitude_to_gmap(self, value):
		position = str(value)
		return str(float(float(position[:3]) + float(position[3:]) / 60))

	def cleanup(self):
		for cs in self.last_heard:
			diff = time.mktime(datetime.now().timetuple()) - time.mktime(self.last_heard[cs]['time'].timetuple())
			if (diff / 60) > 120:
				del self.last_heard[cs]

	# write an html based on the last_heard info.
	def update_output(self):
		html_file = open(self.output_html_file, "w+")
		html_file.write(render_last_heard_html(self.last_heard))
		html_file.close()

if __name__ == "__main__":
	data = {}
	data['slow_speed_data'] = '%b\x85@ElielA, BueBnos ACires ffffffffffffffffffffffffffffffffffff%b\x855$GPGG5A,,34534.285,S,055829.355,W,,5,,1765,M,,,5,,*395\r\n$GP%b\x855RMC,,5A,34354.28,5S,058529.355,W,,,5,,,*354\r\nLU51ALY 5 ,   %b\x855     5     5     4  \r\nf%\x1a\xc6'
	data['rpt2'] = 'LU3AOC G'
	data['sfx'] = 'D74 '
	data['rpt1'] = 'LU3AOC B'
	data['ur'] = 'CQCQCQ  '
	data['message'] = 'Eliel, Buenos Aires '
	data['my'] = 'LU1ALY  '
	data['id'] = 441
	data['gps'] = {}
	data['gps']['$GPGGA'] = '$GPGGA,,3434.28,S,05829.35,W,,,,176,M,,,,,*39'
	data['gps']['$GPRMC'] = '$GPRMC,,A,3434.28,S,05829.35,W,,,,,,*34'
	last = LastHeard()
	last.add(data)
	time.sleep(2)
	last.add(data)
	last.update_output()

