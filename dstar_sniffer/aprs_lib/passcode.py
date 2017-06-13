
# Calculates the callsign passcode.
def passcode_generator(callsign):
	real_callsign = callsign.split("-")[0].upper()
	passcode = 0x73e2
	i = 0
	
	while i+1 < len(real_callsign): 
		passcode ^= ord(real_callsign[i]) << 8
		passcode ^= ord(real_callsign[i+1])
		i += 2

	return str(passcode & 0x7fff)

