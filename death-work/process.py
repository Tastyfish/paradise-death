import sys, csv, string
jobs = {}
jobmap = {}
basemap = {
	"PA": "PAI",
	"MODE": "Unknown"
}

def sanitize(str):
	return string.lstrip(str, "\xc3\xbf\x16").replace("\\", "\\\\").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

def fixjob(job):
	for j in jobs:
		if job == j[:-1]:
			jobmap[job] = j
			return j
	jobmap[job] = job
	return job
	
def cap(word):
	return word[0].upper() + word[1:]

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
		
		jobs[cap(sanitize(row[5]))] = True
		i += 1
	
	newjobs = {}
	for j in jobs:
		newjobs[fixjob(j)] = True
	jobs = newjobs
	
	for before, after in basemap.iteritems():
		del jobs[before]
		jobs[after] = True
		jobmap[before] = after
	
	with open('jobs.json', 'w') as outf:
		outf.write('[')

		i = 0
		for name in jobs.keys():
			if i > 0:
				outf.write(',')
				
			outf.write("\"%s\"" % name)
			i += 1
		outf.write(']')
	
with open('death_csv.csv', 'rb') as inf:
	reader = csv.reader(inf)
	with open('death.json', 'w') as outf:
		outf.write('[')
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
			outf.write("[\"%s\",[%d,%d],%d,\"%s\",%d,\"%s\"]" % (sanitize(row[0]), coords[0], coords[1], int(string.split(row[2], '-')[0]), sanitize(row[3]), 0 if row[4] == "male" else 1, jobmap[cap(sanitize(row[5]))]))
			prevRow = row
			i += 1
		outf.write(']')
