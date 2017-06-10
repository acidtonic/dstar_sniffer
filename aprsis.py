import aprs

def aprs_connect(callsign, password):
	aprs_connection = aprs.TCP(callsign, password)
	aprs_connection.start()
	return aprs_connection
