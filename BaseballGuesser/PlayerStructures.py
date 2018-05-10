import copy

class batStat:
	def __init__(self):
		self.AB = 0
		self.pitches = 0
		self.pitchesOnLine = 0
		self.hits = 0
		self.contacts = 0
		self.battOrder = []
		self.gameCount = 0
		self.gamesInRowWithHit = 0

		self.thisGame = {"AB": 0, "pitches": 0, "pitchesOnLine": 0, "hits": 0, "contacts": 0}
		self.lastGame = {"AB": 0, "pitches": 0, "pitchesOnLine": 0, "hits": 0, "contacts": 0}
		#Contains: AB, pitches, pitchesOnLine, hits, contacts

		#tempStoreValue
		self.gotHit = False

	def getStatRack(self):
		#zero checks
		if (self.AB) == 0:
			val1 = 0
			val3 = 0
		else:
			val1 = float(self.hits)/float(self.AB)
			val3 = float(self.contacts)/float(self.AB)

		if (self.pitches) == 0:
			val2 = 0
			val4 = 0
		else:
			val2 = float(self.hits)/float(self.pitches)
			val4 = float(self.contacts)/float(self.pitches)

		return [val1, val2, val3, val4, self.gamesInRowWithHit]

	def getOldStatRack(self):
		#zero checks
		if (self.lastGame["AB"]) == 0:
			val1 = 0
			val3 = 0
		else:
			val1 = float(self.lastGame["hits"])/float(self.lastGame["AB"])
			val3 = float(self.lastGame["contacts"])/float(self.lastGame["AB"])

		if (self.lastGame["pitches"]) == 0:
			val2 = 0
			val4 = 0
		else:
			val2 = float(self.lastGame["hits"])/float(self.lastGame["pitches"])
			val4 = float(self.lastGame["contacts"])/float(self.lastGame["pitches"])

		return [val1, val2, val3, val4]

	def addGameStats(self):
		self.AB += self.thisGame['AB']
		self.pitches += self.thisGame['pitches']
		self.pitchesOnLine += self.thisGame['pitchesOnLine']
		self.hits += self.thisGame['hits']
		self.contacts += self.thisGame['contacts']

	def makeHistoric(self):
		self.addGameStats()
		self.lastGame = copy.deepcopy(self.thisGame)
		self.thisGame = {"AB": 0, "pitches": 0, "pitchesOnLine": 0, "hits": 0, "contacts": 0}

	def __str__(self):
		listBuilder = []
		listBuilder.append(self.AB)
		listBuilder.append(self.pitches)
		listBuilder.append(self.pitchesOnLine)
		listBuilder.append(self.hits)
		listBuilder.append(self.contacts)
		listBuilder.append(self.battOrder)
		listBuilder.append(self.gameCount)
		listBuilder.append(self.gamesInRowWithHit)

		listBuilderThis = []
		listBuilderThis.append(self.thisGame["AB"])
		listBuilderThis.append(self.thisGame["pitches"])
		listBuilderThis.append(self.thisGame["pitchesOnLine"])
		listBuilderThis.append(self.thisGame["hits"])
		listBuilderThis.append(self.thisGame["contacts"])

		listBuilder.append(listBuilderThis)

		listBuilderLast = []
		listBuilderLast.append(self.lastGame["AB"])
		listBuilderLast.append(self.lastGame["pitches"])
		listBuilderLast.append(self.lastGame["pitchesOnLine"])
		listBuilderLast.append(self.lastGame["hits"])
		listBuilderLast.append(self.lastGame["contacts"])

		listBuilder.append(listBuilderLast)

		return str(listBuilder)

	def rebuild(self, definition):
		r = eval(definition)
		self.AB = r[0]
		self.pitches = r[1]
		self.pitchesOnLine = r[2]
		self.hits = r[3]
		self.contacts = r[4]
		self.battOrder = r[5]
		self.gameCount = r[6]
		self.gamesInRowWithHit = r[7]

		r2 = r[8]
		self.thisGame["AB"] = r2[0]
		self.thisGame["pitches"] = r2[1]
		self.thisGame["pitchesOnLine"] = r2[2]
		self.thisGame["hits"] = r2[3]
		self.thisGame["contacts"] = r2[4]

		r3 = r[9]
		self.lastGame["AB"] = r3[0]
		self.lastGame["pitches"] = r3[1]
		self.lastGame["pitchesOnLine"] = r3[2]
		self.lastGame["hits"] = r3[3]
		self.lastGame["contacts"] = r3[4]

class Batter:
	def __init__(self):
		self.stats = batStat()
		self.teamWins = 0
		self.teamLosses = 0
		self.pitchers = {}

	def __str__(self):
		outputs = []
		outputs.append(str(self.stats))
		for k in self.pitchers:
			outputs.append([k,str(self.pitchers[k])])

		return str(outputs)

	def rebuild(self, definition):
		r = eval(definition)
		self.stats.rebuild(r[0])

		if (len(r) >= 1):
			for n in range(1,len(r)):
				temp = batStat()
				temp.rebuild(r[n][1])
				self.pitchers[r[n][0]] = temp



class pitchStat:
	def __init__(self):
		self.pitches = 0
		self.hitsAllowed = 0
		self.IP = 0
		self.gamesStarted = 0
		self.gameCount = 0
		self.teamWins = 0
		self.teamLosses = 0

		self.thisGame = {"pitches": 0, "hitsAllowed": 0, "IP": 0}
		self.lastGame = {"pitches": 0, "hitsAllowed": 0, "IP": 0}
		#Contains: pitches, hitsAllowed, IP

	def getCumulHPP(self):
		return self.hitsAllowed/self.pitches

	def getStatRack(self):
		if (self.pitches == 0):
			val1 = 0
		else:
			val1 = float(self.hitsAllowed)/float(self.pitches)

		return [val1, self.IP, self.pitches]

	def getOldStatRack(self):
		if (self.lastGame["pitches"] == 0):
			val1 = 0
		else:
			val1 = float(self.lastGame["hitsAllowed"])/float(self.lastGame["pitches"])

		return [val1, self.lastGame["IP"], self.lastGame["pitches"]]

	def addGameStats(self):
		self.pitches += self.thisGame['pitches']
		self.hitsAllowed += self.thisGame['hitsAllowed']
		self.IP+= self.thisGame['IP']

	def makeHistoric(self):
		self.addGameStats()
		self.lastGame = copy.deepcopy(self.thisGame)
		self.thisGame = {"pitches": 0, "hitsAllowed": 0, "IP": 0}

	def __str__(self):
		listBuilder = []
		listBuilder.append(self.pitches)
		listBuilder.append(self.hitsAllowed)
		listBuilder.append(self.IP)
		listBuilder.append(self.gamesStarted)
		listBuilder.append(self.gameCount)
		listBuilder.append(self.teamWins)
		listBuilder.append(self.teamLosses)

		listBuilderThis = []
		listBuilderThis.append(self.thisGame["pitches"])
		listBuilderThis.append(self.thisGame["hitsAllowed"])
		listBuilderThis.append(self.thisGame["IP"])

		listBuilder.append(listBuilderThis)

		listBuilderLast = []
		listBuilderLast.append(self.lastGame["pitches"])
		listBuilderLast.append(self.lastGame["hitsAllowed"])
		listBuilderLast.append(self.lastGame["IP"])

		listBuilder.append(listBuilderLast)

		return str(listBuilder)

	def rebuild(self, definition):
		r = eval(definition)
		self.pitches = r[0]
		self.hitsAllowed = r[1]
		self.IP = r[2]
		self.gamesStarted = r[3]
		self.gameCount = r[4]
		self.teamWins = r[5]
		self.teamLosses = r[6]

		r2 = r[7]
		self.thisGame["pitches"] = r2[0]
		self.thisGame["hitsAllowed"] = r2[1]
		self.thisGame["IP"] = r2[2]

		r3 = r[8]
		self.lastGame["pitches"] = r2[0]
		self.lastGame["hitsAllowed"] = r2[1]
		self.lastGame["IP"] = r2[2]

class Pitcher:
	def __init__(self):
		self.stats = pitchStat()

	def __str__(self):
		return str(self.stats)

	def rebuild(self, definition):
		self.stats = pitchStat()
		self.stats.rebuild(definition)
