import ConfigParser

def config_load():
	# Read configuration file.
	config = ConfigParser.ConfigParser()
	config.read("/etc/dstar_sniffer/dstar_sniffer.conf")
	return config

