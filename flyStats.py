import parser as kmlParser
import argparse
import os
import re
from datetime import date, time
import sys

class Fly:
	def __init__(self):
		self.duration = None
		self.takeOffAltitude = None
		self.landingAltitude = None
		self.maxAltitude = None
		self.date = None
		self.maxSpeed = None
		self.maxG = None
		self.begin = None
		self.end = None

	def __lt__(self, other):
		return self.date < other.date or (self.date == other.date and self.begin < other.begin)

def formatTime(sec):
	h = str(sec/3600)
	m = str((sec%3600)/60)
	s = str(sec%60)
	return (h if len(h)==2 else ' '+h)+'h'+(m if len(m)==2 else '0'+m)+'m'+(s if len(s)==2 else '0'+s)+'s'

def listKml(path):
	return map(lambda x: path+x, filter(lambda f : f.endswith('.kml'), os.listdir(path)))

def listRecKml(path):
	listKmlFile = []
	for fileName in os.listdir(path):
		if(os.path.isdir(path+fileName)):
			listKmlFile += listRecKml(path + fileName +'/')
	return listKmlFile + listKml(path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run into KML gps traces')
	parser.add_argument("-d", "--dir", help="Directory wich contains KML gps traces", required=True)
	parser.add_argument("-r", "--rec", help="Recursion search", action='store_true')
	args = parser.parse_args()

	directoryPath = args.dir
	if(not directoryPath.endswith('/')):
		directoryPath += '/'
	
	if(args.rec):
		kmlFilesNames = listRecKml(directoryPath)
	else:
		kmlFilesNames = listKml(directoryPath)
	numberOfFlies = len(kmlFilesNames)

	regexDate = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
	regexDuration = re.compile('Duration: ([0-9]{2})h([0-9]{2})m([0-9]{2})s')
	regexMaxSpeed = re.compile('Max speed [0-9]{1,2}:[0-9]{1,2}: ([0-9]+\.[0-9]+) km\/h')
	regexMaxG = re.compile('Max G force [0-9]{1,2}:[0-9]{1,2}: ([0-9]+\.[0-9]+) G')
	regexMaxAltitude = re.compile('Max Altitude [0-9]{1,2}:[0-9]{1,2}: ([0-9]+) m')
	regexCoordinate = re.compile('([0-9]+\.[0-9]+),([0-9]+\.[0-9]+),([0-9]+\.[0-9]+)')

	maxSpeed = 0
	maxG = 0
	maxDuration = 0
	averageDuration = 0
	minDuration = sys.maxint
	totalDuration = 0
	minDay = date.max
	maxDay = date.min
	earlier = sys.maxint
	latest = 0
	higher = 0
	flies = []

	for kmlFileName in kmlFilesNames:
		fly = Fly()
		kml = kmlParser.parse(kmlFileName)
		for placemark in kml.getroot().Document.Placemark:
			if(regexDate.match(str(placemark.name))):
				placemarkDate = placemark
				placemarkTrace = placemark
				placemarkMaxAltitude = placemark
			if(str(placemark.name).startswith('Duration: ')):
				placemarkDuration = placemark
			if(str(placemark.name).startswith('Takeoff: ')):
				placemarkTakeoff = placemark
			if(str(placemark.name).startswith('Landing: ')):
				placemarkLanding = placemark
			if(str(placemark.name).startswith('Max speed')):
				placemarkMaxSpeed = placemark
			if(str(placemark.name).startswith('Max G force')):
				placemarkMaxG = placemark

		# Date
		if(placemarkDate is not None):
			dateSplited = map(lambda x: int(x), str(placemarkDate.name).split('-'))
			captureDate = date(dateSplited[0], dateSplited[1], dateSplited[2])
			fly.date = captureDate
			if(captureDate < minDay):
				minDay = captureDate
			if(captureDate > maxDay):
				maxDay = captureDate
	
		# Duration
		if(placemarkDuration is not None):
			matchDuration = regexDuration.finditer(str(placemarkDuration.name)).next()
			duration = int(matchDuration.group(1)) * 3600 + int(matchDuration.group(2)) * 60 + int(matchDuration.group(3))
			fly.duration = duration
			totalDuration += duration
			if(duration < minDuration):
				minDuration = duration
			if(duration > maxDuration):
				maxDuration = duration

		# Begin
		if(placemarkTakeoff is not None):
			tmpTakeoff = str(placemarkTakeoff.name).split(':')
			fly.begin = 3600 * int(tmpTakeoff[1]) + 60 * int(tmpTakeoff[2])
			if(fly.begin < earlier):
				earlier = fly.begin

		# End
		if(placemarkLanding is not None):
			tmpLanding = str(placemarkLanding.name).split(':')
			fly.end = 3600 * int(tmpLanding[1]) + 60 * int(tmpLanding[2])
			if(fly.end > latest):
				latest = fly.end

		# Max speed
		if(placemarkMaxSpeed is not None):
			matchMaxSpeed = regexMaxSpeed.finditer(str(placemarkMaxSpeed.name)).next()
			fly.maxSpeed = float(matchMaxSpeed.group(1))
			if(fly.maxSpeed > maxSpeed):
				maxSpeed = fly.maxSpeed

		# Max G
		if(placemarkMaxG is not None):
			matchMaxG = regexMaxG.finditer(str(placemarkMaxG.name)).next()
			fly.maxG = float(matchMaxG.group(1))
			if(fly.maxG > maxG):
				maxG = fly.maxG

		# Max Altitude
		if(placemarkMaxAltitude is not None):
			coordinates = str(placemarkTrace.LineString.coordinates)
			altitudes = []
			for coordinate in coordinates.split('\n'):
				if(len(coordinate)):
					matchMaxAltitude = regexCoordinate.finditer(coordinate).next()
					altitudes.append(int(float(matchMaxAltitude.group(3)))+1)
			fly.maxAltitude = max(altitudes)
			if(fly.maxAltitude > higher):
				higher = fly.maxAltitude

		# Takeoff Altitude
		if(placemarkTrace is not None):
			coordinates = str(placemarkTrace.LineString.coordinates)
			takeoffCoordinate = coordinates[:coordinates[1:].find('\n')]
			matchTakeoffAltitude = regexCoordinate.finditer(takeoffCoordinate).next()
			fly.takeoffAltitude = int(float(matchTakeoffAltitude.group(3)))+1

		# Landing Altitude
		if(placemarkTrace is not None):
			coordinates = str(placemarkTrace.LineString.coordinates)
			landingCoordinate = coordinates[coordinates[:-1].rfind('\n'):]
			matchLandingAltitude = regexCoordinate.finditer(landingCoordinate).next()
			fly.landingAltitude = int(float(matchLandingAltitude.group(3)))+1

		flies.append(fly)
	
	averageDuration = totalDuration / numberOfFlies
	flies = sorted(flies)

	print "===== Statistiques de vols ====="
	print "Du "+minDay.strftime("%d/%m/%y")+" au "+maxDay.strftime("%d/%m/%y")
	print str(numberOfFlies)+' vols'
	print 'Temps de vol total: '+formatTime(totalDuration)
	print 'Temps de vol minimum: '+formatTime(minDuration)
	print 'Temps de vol maximum: '+formatTime(maxDuration)
	print 'Temps de vol moyen: '+formatTime(averageDuration)
	print 'Le vol le plus tot: '+formatTime(earlier)
	print 'Le vol le plus tard: '+formatTime(latest)
	print 'La plus haute vitesse: '+str(maxSpeed)+'km/h'
	print 'La plus haute force G: '+str(maxG)+'g'
	print 'La plus haute altitude: '+str(higher)+'m'

	print '|--------|---------|---------|---------|---------|-----|-----|-----|-----|'
	print '|  Date  |  Duree  |Decollage| Arrivee |  Vit M  |Max G|Alt M|Alt D|Alt A|'
	print '|--------|---------|---------|---------|---------|-----|-----|-----|-----|'
	for fly in flies:
		print '|'+fly.date.strftime("%d/%m/%y")+'|'+formatTime(fly.duration)+'|'+formatTime(fly.begin)+'|'+formatTime(fly.end)+'|'+"%05.2fkm/h" % fly.maxSpeed+'|'+ "%.2fg" % fly.maxG+'|'+ ' '*(4-len(str(fly.maxAltitude)))+str(fly.maxAltitude)+'m|'+ ' '*(4-len(str(fly.takeoffAltitude)))+str(fly.takeoffAltitude)+'m|'+' '*(4-len(str(fly.landingAltitude))) + str(fly.landingAltitude)+'m|'
	print '|--------|---------|---------|---------|---------|-----|-----|-----|-----|'
