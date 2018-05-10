#Apparently you need to run using python not python3

import urllib
import PlayerStructures

from bs4 import BeautifulSoup
import copy
import time
import random
import csv

batters = {}
pitchers = {}



#import existing values
#import Pitchers
previousYear = "2017"

with open("data/pitcherExtracts_" + previousYear + ".csv", "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		rowString = row[0]
		pitcherName,pitcherData = rowString.split("|")

		pitchers[pitcherName] = PlayerStructures.Pitcher()
		pitchers[pitcherName].rebuild(pitcherData)

f.close()

#import Batters
with open("data/batterExtracts_" + previousYear + ".csv", "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		rowString = row[0]
		batterName,batterData = rowString.split("|")

		batters[batterName] = PlayerStructures.Batter()
		batters[batterName].rebuild(batterData)

f.close()

for batter in batters:
	print(batter)

for pitcher in pitchers:
	print(pitcher)

print(len(batters))
print(len(pitchers))




#years = ["2012", "2013","2014","2015","2016","2017"]
years = ["2018"]

for year in years:
	#Works
	url = 'https://www.baseball-reference.com/leagues/MLB/' + year + '-schedule.shtml'
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html,'lxml')
	htmlgames = soup.find_all("p", class_="game")

	seasonGames = []
	for htmlgame in htmlgames:
		#URL looks like /previews/... if the game has not happened
		if (htmlgame.em.a['href'].split("/")[1] == "previews"):
			break

		print(htmlgame.em.a['href'])
		seasonGames.append('https://www.baseball-reference.com' + htmlgame.em.a['href'])



	'''
	testURL = 'https://www.baseball-reference.com/boxes/ANA/ANA201004050.shtml'
	html = urllib.urlopen(testURL).read()
	soup = BeautifulSoup(html,'lxml')

	temp = soup.find(id="all_play_by_play")
	cutOutTable = str(temp)[str(temp).find("<!--")+4:str(temp).find("-->")]
	tableSoup = BeautifulSoup(cutOutTable,'lxml')
	table = [[td.text.encode("utf-8") for td in row.find_all("td")] for row in tableSoup.select("tr + tr")]

	for line in table:
		if (len(line) > 0):
			if (not line[0]==""):
				print(line)

	#testing
	#seasonGames = []
	#seasonGames.append('https://www.baseball-reference.com/boxes/TBA/TBA201803290.shtml')
	'''



	descriptColumn = 10
	batterCol = 6
	pitcherCol = 7
	pitchCol = 3
	ROCol = 4
	outsCol = 2


	entries = []
	#entry = ["Batter","Pitcher","NUMHITSCURRENT","Hits","AB","Contacts","Total Pitches Recieve by Batter","Total PitchesOnLine to Batter","Hits per AB","Hits per pitch","Contacts per AB","Contacts per pitch","Game in row with hit","Hits per AB-pp","Contacts per AB-pp","Hits per pitch-pp","Contacts per pitch-pp","Game in row with hit-pp","Hits per AB-lg","Hits per pitch-lg","Contacts per AB-lg", "Contacts per pitch-lg", "Hits per AB-lg-pp","Hits per pitch-lg-pp","Contacts per AB-lg-pp","Contacts per pitch-lg-pp","Hits Per Pitch", "Innings Pitched", "Pitches","Hits Per Pitch-lg","Innings Pitched-lg","Pitches-lg", "dateOfGame", "timeOfGame", "startWeather"]

	#entries.append(entry)
	print("Starting:-------" + year)
	counter = 0
	for game in seasonGames:
		counter += 1
		print("     " + str(counter) + "|" + str(len(seasonGames)))

		#randomTime
		time.sleep(random.random()*10)
		try:
			html = urllib.urlopen(game).read()
		except:
			print("Failed Game: " + game)
			continue

		soup = BeautifulSoup(html,'lxml')


		try:
			dateOfGame = soup.find_all("div", class_="scorebox")[0].find_all("div")[13].get_text()
			timeOfGame = soup.find_all("div", class_="scorebox")[0].find_all("div")[18].get_text().split(" ")[0]

			cutToEnd = str(soup.find('body').find_all("span", {"data-label": "Other Info"})[0].parent.parent)[str(soup.find('body').find_all("span", {"data-label": "Other Info"})[0].parent.parent).find("<strong>Start Time Weather:</strong>")+36:]
			startWeather = cutToEnd[:cutToEnd.find("<")]


			#div class scorebox > div (visitors), div (home) > div, div, div (record)
			recordVisitors = soup.find_all("div", class_="scorebox")[0].find_all("div")[4].get_text().split("-")
			recordHome = soup.find_all("div", class_="scorebox")[0].find_all("div")[10].get_text().split("-")

			temp = soup.find(id="all_play_by_play")
			cutOutTable = str(temp)[str(temp).find("<!--")+4:str(temp).find("-->")]
			tableSoup = BeautifulSoup(cutOutTable,'lxml')
			table = [[td.text.encode("utf-8") for td in row.find_all("td")] for row in tableSoup.select("tr + tr")]

			gamePitchers = []
			gameBatters = []

			lastOuts = -1
			gameStartedH = ""
			gameStartedV = ""
			for line in table:
				if (len(line) > 0):
					if (not (line[0]=="" or line[batterCol]=="" or line[pitcherCol]=="" or line[pitchCol]=="")):

						#getBatter
						batterEntry = line[batterCol]
						batterEntry = batterEntry.replace("\xc2\xa0"," ")

						#getPitcher
						pitcherEntry = line[pitcherCol]
						pitcherEntry = pitcherEntry.replace("\xc2\xa0"," ")

						if (not batterEntry in batters):
							batters[batterEntry] = PlayerStructures.Batter()

						tempBatter = batters[batterEntry]

						if (not pitcherEntry in tempBatter.pitchers):
							tempBatter.pitchers[pitcherEntry] = PlayerStructures.batStat()

						if (not batterEntry in gameBatters):
							gameBatters.append(batterEntry)


						if (not pitcherEntry in pitchers):
							pitchers[pitcherEntry] = PlayerStructures.Pitcher()

						tempPitcher = pitchers[pitcherEntry]

						if (not pitcherEntry in gamePitchers):
							gamePitchers.append(pitcherEntry)

						#collectData
						pitchesEntry = line[pitchCol]
						pitchesEntry = pitchesEntry.replace("\xc2\xa0"," ")
						pitchVal = pitchesEntry.split(",")[0]
						if (pitchVal == ""):
							numPitches = 0
						else:
							numPitches = int(pitchVal)
						pitchesOnLine = int(pitchesEntry.split("-")[-1][0]) #value right after - is strikes
						runsAndOuts = line[ROCol]
						desc = line[descriptColumn]
						outs = line[outsCol]

						newInning = False
						if (lastOuts == -1):
							newInning = True
							gameStartedH = pitcherEntry

						if (outs < lastOuts):
							newInning = True
							if (gameStartedV == ""):
								gameStartedV = pitcherEntry

						lastOuts = outs

						#calc hit/contact
						contact = False
						hit = False
						if ("X" in pitchesEntry):
							contact = True
							pitchesOnLine += 1
							if (not "O" in runsAndOuts) and (not "Fielder's choice" in desc):
								hit = True
							#when they hit and stay in but someone else gets out
							if ("O" in runsAndOuts) and ("OO" not in runsAndOuts) and (" out" in desc):
								hit = True

						#update stats
						if (hit):
							tempBatter.stats.thisGame["hits"] += 1
							tempBatter.pitchers[pitcherEntry].thisGame["hits"] += 1
							tempPitcher.stats.thisGame["hitsAllowed"] += 1

						if (contact):
							tempBatter.stats.thisGame["contacts"] += 1
							tempBatter.pitchers[pitcherEntry].thisGame["contacts"] += 1

						if (newInning):
							tempPitcher.stats.thisGame["IP"] += 1


						tempBatter.stats.thisGame["pitches"] += numPitches
						tempBatter.stats.thisGame["AB"] += 1
						tempBatter.stats.thisGame["pitchesOnLine"] += pitchesOnLine

						tempBatter.pitchers[pitcherEntry].thisGame["pitches"] += numPitches
						tempBatter.pitchers[pitcherEntry].thisGame["AB"] += 1
						#print(batterEntry + "_" + pitcherEntry + ": " + str(tempBatter.pitchers[pitcherEntry].thisGame["AB"]))
						tempBatter.pitchers[pitcherEntry].thisGame["pitchesOnLine"] += pitchesOnLine

						tempPitcher.stats.thisGame["pitches"] += numPitches


			#create entries BEFORE updating stats (how did they perform as predictable by previous stats)

			for game_batter in gameBatters:
				for game_pitcher in gamePitchers:
					if ((game_pitcher in batters[game_batter].pitchers) and (batters[game_batter].pitchers[game_pitcher].thisGame["AB"] > 0)):
						entryHit = 0
						if batters[game_batter].pitchers[game_pitcher].thisGame["hits"] > 0:
							entryHit = batters[game_batter].pitchers[game_pitcher].thisGame["hits"]

						entry = [game_batter, game_pitcher, copy.deepcopy(entryHit), batters[game_batter].stats.hits, batters[game_batter].stats.AB, batters[game_batter].stats.contacts, batters[game_batter].stats.pitches, batters[game_batter].stats.pitchesOnLine] + batters[game_batter].stats.getStatRack() + batters[game_batter].pitchers[game_pitcher].getStatRack() + batters[game_batter].stats.getOldStatRack() + batters[game_batter].pitchers[game_pitcher].getOldStatRack() + pitchers[game_pitcher].stats.getStatRack() + pitchers[game_pitcher].stats.getOldStatRack() + [dateOfGame, timeOfGame, startWeather]
						entries.append(entry)

						#Entry Made, Clean Game
						if batters[game_batter].pitchers[game_pitcher].thisGame["hits"] > 0:
							batters[game_batter].pitchers[game_pitcher].gamesInRowWithHit += 1
						else:
							batters[game_batter].pitchers[game_pitcher].gamesInRowWithHit = 0

						batters[game_batter].pitchers[game_pitcher].makeHistoric()


				#entries for this batter made. Clean Game
				if batters[game_batter].stats.thisGame["hits"] > 0:
					batters[game_batter].stats.gamesInRowWithHit += 1
				else:
					batters[game_batter].stats.gamesInRowWithHit = 0

				#add starting pitchers
				pitchers[gameStartedH].stats.gamesStarted += 1
				pitchers[gameStartedV].stats.gamesStarted += 1
				batters[game_batter].stats.makeHistoric()


			for game_pitcher in gamePitchers:
				pitchers[game_pitcher].stats.makeHistoric()

		except:
			print("Failed Game: " + game)
			continue


	#final write out after ALL collection is done
	batterWriteOuts = []
	for batter in batters:
		batterWriteOuts.append([batter + "|" + str(batters[batter])])

	pitcherWriteOuts = []
	for pitcher in pitchers:
		pitcherWriteOuts.append([pitcher + "|" + str(pitchers[pitcher])])


	with open("data/output_" + year + ".csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(entries)
	f.close()

	with open("data/batterExtracts_" + year + ".csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(batterWriteOuts)
	f.close()

	with open("data/pitcherExtracts_" + year + ".csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(pitcherWriteOuts)
	f.close()
