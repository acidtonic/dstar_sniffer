import re

def gpgga_get_position(gpgga_sentence):
	sentence = gpgga_sentence.split(",") 
	position = {}
	position['lat'] = sentence[2]
	position['lat_coord'] = sentence[3]
	position['long'] = sentence[4]
	position['long_coord'] = sentence[5]
	if len(sentence[11]) > 0:
		position['height'] = str(int(float(sentence[11]) * 3.28084)).zfill(6)
	return position

def dprs_get_position(dprs_sentence):
	pos = re.match(".+:!([0-9]{4}\.[0-9]{2})([SN]).([0-9]{5}\.[0-9]{2})([EW]).+", dprs_sentence)
	position = {}
	position['lat'] = pos.group(1)
	position['lat_coord'] = pos.group(2)
	position['long'] = pos.group(3)
	position['long_coord'] = pos.group(4)
	return position

if __name__ == "__main__":
	print dprs_get_position("LU1ALY-7>API51,DSTAR*:!3434.27S/05829.35W[/A=000083ELIEL")

