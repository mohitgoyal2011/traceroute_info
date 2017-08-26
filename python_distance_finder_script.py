import commands
import os
import sys
import json
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import time as ti

distance = []
time = []
my_location = '28.535516,77.391026'
my_location_tuple = (float(my_location.split(',')[0]),float(my_location.split(',')[1]))
geolocator = Nominatim()

if sys.argv[2] and sys.argv[2] == 'all':
	argument = sys.argv[1].split('.')[0]
	output = commands.getoutput('traceroute ' + sys.argv[1] + ' > ' + argument + '_morning_data')
	print output
	f = open(sys.argv[1].split('.')[0] + '_morning_data')
	fw = open(sys.argv[1].split('.')[0] + '_morning_ip_data','w')
	fw.write('Traceroute information for ' + sys.argv[1] + '\n')
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		comps = line.split(' ')
		print comps
	
		if comps[0] == 'traceroute':
			continue
		if '* * *' in line:
			continue
		length = len(comps)
		i = 0
		while i < length:
			if comps[i] == '' or comps[i] == '*':
				del comps[i]
				length = length - 1
			i = i + 1
		print comps
		serial_no = int(comps[0])
		avg_sum = 0.0
		count = 0.0
		for i in range(0,len(comps)):
			if i<len(comps)-1 and comps[i+1] == 'ms':
				avg_sum = avg_sum + float(comps[i])
				count = count + 1		
		average_delay = (avg_sum/count)/2.0
		ip_address = comps[2].strip('(').strip(')')
		output = commands.getoutput('curl -s ipinfo.io/' + ip_address)
		print output
		json_dic = json.loads(output)
		if 'loc' not in json_dic.keys():
			location = my_location
		else:
			location = json_dic["loc"]

		ti.sleep(5)
		if location == my_location:
			city = '3G1, ATS Greens II, Sector 50, Noida, UP, 201307, India'
		else:
			loc = geolocator.reverse(location)
			city = loc.address	
		latitude = float(location.split(',')[0])
		longitude = float(location.split(',')[1])
		dist = (vincenty((latitude,longitude),my_location_tuple).miles)
		fw.write(str(serial_no) + ' ' + ip_address + ' ' + location + ' ' + str(average_delay) + ' ' + str(dist) + ' ' + city.__repr__() + '\n')

	fw.close()

fw = open(sys.argv[1].split('.')[0] + '_morning_ip_data')
lines = fw.readlines()
for line in lines[1:]:
	comps = line.split(' ')
	print comps
	latitude = float(comps[2].split(',')[0])
	longitude = float(comps[2].split(',')[1])
	distance.append(float(comps[4]))
	time.append(float(comps[3]))
distance.sort()
[x for (y,x) in sorted(zip(time,distance))]
plt.xlabel('Distance (Miles)')
plt.ylabel('Time (Milliseconds)')
plt.title('Distance vs Average One Way Delay for ' + sys.argv[1])
plt.plot(distance, time, '--')
plt.savefig(sys.argv[1].split('.')[0] + '_morning.png')
	
	

