#!/usr/bin/env python

#
# DSTAR Repeater Controller Sniffer
#
# Coded by Eliel Sardanons (LU1ALY)
#

import socket
import sys
import logging
import logging.config

from dstar_lib import DStar, last_heard_callback
from aprs_lib import aprsis_dstar_callback
from net_lib import parse_packet
from util_lib.daemon import Daemon
from util_lib import config

class DStarSniffer(Daemon):
	def run(self):
		# Setup logging
		logging.config.fileConfig('/etc/dstar_sniffer/logging.conf')
		logger = logging.getLogger(__name__)
		logger.info("DStar Sniffer started.")

		# Read configuration file.
		cfg = config.config_load()
		controller_ip = cfg.get("controller", "ip")
		controller_port = cfg.getint("controller", "port")
		controller_iface = cfg.get("controller", "iface")

		# Initialize the dstar packet manipulation class
		dstar = DStar()
		dstar_tocontroller = DStar()

		# Register a dstar stream callback, this will
		# be executed once we parse the full dstar stream.
		dstar_stream_callback = []
		dstar_stream_callback.append(aprsis_dstar_callback) # Upload received positions to APRS-IS
		dstar_stream_callback.append(last_heard_callback) # Record last heard stations

		try:
			# Start listening to every UDP packet.
			s = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
			s.setsockopt(socket.SOL_SOCKET, 25, controller_iface) # Bind to device
		except socket.error , msg:
			logger.error('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
			sys.exit(-1)

		# Main loop, receive udp packets and run callbacks
		while True:
			try:
				packet = s.recvfrom(65565)
				data = parse_packet(packet, source_ip = controller_ip, destination_port = controller_port)
				if data != None:
					dstar_stream = dstar.parse(data)
					if dstar_stream != None:
						# End of stream!
						logger.info(dstar_stream)
						logger.info("STREAM[%s] UR[%s] MY[%s] RPT1[%s] RPT2[%s] MESSAGE[%s]" % (dstar_stream['id'],dstar_stream['ur'], dstar_stream['my'],\
						dstar_stream['rpt1'], dstar_stream['rpt2'], dstar_stream['message']))
						logger.info("Start running callbacks for received stream [%s]", dstar_stream['id'])
						for cb in dstar_stream_callback:
							logger.debug("Running callback: %s" % str(cb.__name__))
							try:
								cb(dstar_stream)
							except Exception, e:
								logger.error(str(e))
						logger.info("End running callbacks for received stream [%s]", dstar_stream['id'])
				else:
					data = parse_packet(packet, destination_port = 20000, destination_ip = controller_ip)
					if data != None:
						dstar_stream_tocontroller = dstar_tocontroller.parse(data)
						logger.debug("UDP stream to_controller: %s" % (dstar_stream_tocontroller))
			except Exception, e:
				logger.error(str(e))
		logger.info("DStar sniffer ends running.")

def main():
	daemon = DStarSniffer('/var/run/dstar_sniffer.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
