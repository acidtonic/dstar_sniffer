import re

def gpgga_get_position(gpgga_sentence):
	sentence = gpgga_sentence.split(",") 
	position = {}
	position['lat'] = sentence[2]
	position['lat_coord'] = sentence[3]
	position['lon'] = sentence[4]
	position['lon_coord'] = sentence[5]
	position['height'] = str(int(float(sentence[11]) * 3.28084)).zfill(6)
	return position

if __name__ == "__main__":
	print gpgga_get_position("$GPGGA,142353.00,3436.93,S,05822.72,W,1,06,2.4,55.5,M,13.2,M,,*54")

