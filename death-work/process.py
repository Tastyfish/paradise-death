import sys, csv, string

def sanitize(str):
	return string.lstrip(str, "\xc3\xbf\x16").replace("\\", "\\\\").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

with open('death.json', 'w') as outf:
	outf.write('[')
	with open('death_csv.csv', 'rb') as inf:
		reader = csv.reader(inf)
		i = 0
		prevRow = None
		for row in reader:
			if i == 0:
				i = 1
				continue
			elif row == prevRow:
				 # in some places, there are several duplicate entries in a row
				continue
			
			coords = map(lambda coord: int(coord.strip()), string.split(row[1], ","))
			if coords[2] != 1:
				continue	# not on the station!
				
			if i > 1:
				outf.write(',')
			outf.write("[\"%s\",[%d,%d],%d,\"%s\",%d]" % (sanitize(row[0]), coords[0], coords[1], int(string.split(row[2], '-')[0]), sanitize(row[3]), 0 if row[4] == "male" else 1))
			prevRow = row
			i += 1
	outf.write(']')
