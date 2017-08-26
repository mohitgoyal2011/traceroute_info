import tabulate
import sys

fw = open(sys.argv[1])
lines = fw.readlines()
table = []
headers = ['Hop', 'IP', 'Location (Latitude, Logitude)', 'Average One Way Delay in msec', 'Distance in kilometers', 'City', 'Propagation Delay', 'Non Propagation Delay']
for line in lines:
	line = line.split(' ', 5)
	if len(line) >=5:
		city = line[5].split(',')[-5] + ',' + line[5].split(',')[-3]
		line[4] = str(float(line[4])*1.6)
		prop_delay = (float(line[4])/(200000.0))*1000
		non_prop_delay = float(line[3]) - prop_delay
		#print line[0]+'::'+line[1]+'::'+line[2]+'::'+ line[3] +'::'+line[4] +'::'+city +'::'+str(prop_delay) +'::'+str(non_prop_delay)
		table.append([line[0],line[1],line[2],line[3],line[4],city, str(prop_delay), str(non_prop_delay)])

print tabulate.tabulate(table,headers)
