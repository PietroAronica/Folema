import random
import copy
import itertools
import operator
import math
from bisect import bisect as _bisect
from itertools import repeat as _repeat
import tabulate

def accumulate(iterable, func=operator.add, initial=None):
    'Return running totals'
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        total = func(total, element)
        yield total

def choices(population, weights=None):
	n = len(population)
	if weights is None:
		floor = _floor
		n += 0.0
		return [population[floor(random.random() * n)] for i in _repeat(None, 1)]
	cum_weights = list(accumulate(weights))
	total = cum_weights[-1] + 0.0
	bisect = _bisect
	hi = n - 1
	return [population[bisect(cum_weights, random.random() * total, 0, hi)]
		for i in _repeat(None, 1)]

#def choices(self, population, weights=None, *, cum_weights=None, k=1):
#	"""Return a k sized list of population elements chosen with replacement.
#	If the relative weights or cumulative weights are not specified,
#	the selections are made with equal probability.
#	"""
#	random = self.random
#	n = len(population)
#	if cum_weights is None:
#		if weights is None:
#			floor = _floor
#			n += 0.0    # convert to float for a small speed improvement
#			return [population[floor(random() * n)] for i in _repeat(None, k)]
#		cum_weights = list(_accumulate(weights))
#	elif weights is not None:
#		raise TypeError('Cannot specify both weights and cumulative weights')
#	if len(cum_weights) != n:
#		raise ValueError('The number of weights does not match the population')
#	total = cum_weights[-1] + 0.0   # convert to float
#	if total <= 0.0:
#		raise ValueError('Total of weights must be greater than zero')
#	if not _isfinite(total):
#		raise ValueError('Total of weights must be finite')
#	bisect = _bisect
#	hi = n - 1
#	return [population[bisect(cum_weights, random() * total, 0, hi)]
#		for i in _repeat(None, k)]

class Table(object):
	def __init__(self, teams):
		self.teams = {}
		for sq in teams:
			self.teams[sq.getname()] = [0,0,0,0,0,0,0,0]

	def update_table(self, team, points, gamesplayed, gameswon, gameslost, gamesdrawn, goalsfor, goalsagainst):
		curr_points = self.teams[team.getname()][0]
		curr_gamesplayed = self.teams[team.getname()][1]
		curr_gameswon = self.teams[team.getname()][2]
		curr_gameslost = self.teams[team.getname()][3]
		curr_gamesdrawn = self.teams[team.getname()][4]
		curr_goalfor = self.teams[team.getname()][5]
		curr_goalagainst = self.teams[team.getname()][6]
		curr_goaldiff = self.teams[team.getname()][7]
		self.teams[team.getname()] = [curr_points+points,curr_gamesplayed+gamesplayed,curr_gameswon+gameswon,curr_gameslost+gameslost,curr_gamesdrawn+gamesdrawn,curr_goalfor+goalsfor,curr_goalagainst+goalsagainst,curr_goaldiff+(goalsfor-goalsagainst)]

	def display_table(self):
		headers = ["Team", "P", "GP", "W", "L", "D", "GF", "GA", "Diff"]
		print(tabulate.tabulate(sorted(sorted(sorted(sorted([[k] + v for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True), headers = headers))

class Team(object):
	def __init__(self, name, strength):
		self.name = name
		self.strength = float(strength)

	def getname(self):
		return self.name

	def getstrength(self):
		return self.strength

class Match(object):
	def __init__(self, hometeam, awayteam):
		self.hometeam = hometeam
		self.awayteam = awayteam

	def gethome(self):
		return self.hometeam
	
	def getaway(self):
		return self.awayteam

	def getread(self):
		return self.gethome() + ' vs ' + self.getaway()

	def getreturn(self):
		return Match(self.getaway(), self.gethome())

class Day(object):
	def __init__(self, number):
		self.number = number
		self.matches = []

	def get_num(self):
		return self.number
	
	def get_matches(self):
		for match in self.matches:
			print match.getread()

	def add_match(self, match):
		self.matches.append(match)

class Year(object):
	def __init__(self, name):
		self.days = {}

	def add_day(self, day):
		num = day.get_num()
		self.days[num] = day

	def get_days(self):
		for num in self.days:
			print num
			self.days[num].get_matches()

def pairwise(items):
	a = iter(items)
	return itertools.izip(a, a)

def makeleague(inputfile):
	dataset = []
	f = open(inputfile)
	opened = f.readlines()
	for line in opened:
		name,strength = line.split(",")
		dataset.append(Team(name.strip(),strength.strip()))
	f.close()
	return dataset

def makecalendar(league):
	if len(league) % 2:
		league.append('Bye')
	rotation = list(league)
	fixtures = []
	for i in range(0, len(league)-1):
		mid = len(rotation) // 2
		l1 = rotation[:mid]
		l2 = rotation[mid:]
		l2.reverse()
		temp = []
		for j in range(mid):
			t1 = l1[j]
			t2 = l2[j]
			if i % 2 == 0:
				temp.append(t1)
				temp.append(t2)
			else:
				temp.append(t2)
				temp.append(t1)
			rotation = rotation[mid:-1] + rotation[:mid] + rotation[-1:]
		fixtures.append(temp)
	matchdays = range(1,len(league))
	year = Year('temp')
	for days in fixtures:
		num = random.choice(matchdays)
		matchdays.remove(num)
		curr_day = Day(num)
		matches = pairwise(days)
		for game in matches:
			curr_match = Match(game[0], game[1])
			curr_day.add_match(curr_match)
		year.add_day(curr_day)
	t = copy.deepcopy(year)
	for d in t.days:
		num = d + (len(league)-1)
		curr_day = Day(num)
		for match in year.days[d].matches:
			new_match = match.getreturn()
			curr_day.add_match(new_match)
		year.add_day(curr_day)
	return year

def playgame(hometeam, awayteam):
	hts = hometeam.getstrength()
	ats = awayteam.getstrength()
	htp = random.randint(0, 6)
	atp = random.randint(0, 5)
	hto = hts*htp
	ato = ats*atp
	if hto - ato > 1:
		htg = int(choices([1,2,3,4,5,6], weights=[30,30,20,4,2,1])[0])
		if hto - ato >= 2:
			htg = htg+1
			atg = htg-1
		if hto - ato >= 4:
			htg = htg+1
#		if ato <= 1:
#			atg = 0
#		else:
		try:
			atg = atg-1
		except:
			atg = htg-1
	elif ato - hto > 1:
		atg = int(choices([1,2,3,4,5,6], weights=[30,30,20,4,2,1])[0])
		if ato - hto >= 2:
			atg = atg+1
			htg = atg-1
		if ato - hto >= 4:
			atg = atg+1
#		if hto <= 1:
#			htg = 0
#		else:
		try:
			htg = htg-1
		except:
			htg = atg-1
	else:
		if ato >= hto:
			atg = math.floor(ato)
			htg = atg
		elif hto > ato:
			htg = math.floor(ato)
			atg = htg
	return hometeam.getname(), int(htg), int(atg), awayteam.getname()

#def playgame(hometeam, awayteam):
	

def gameday(day, table):
	for match in day.matches:
		result = playgame(match.gethome(), match.getaway())
		team1 = result[0]
		ght = result[1]
		gat = result[2]
		team2 = result[3]
		print '{:>20s} {:2} {:2}  {:<20s}'.format(team1, ght, gat, team2)
		if ght > gat:
			table.update_table(match.gethome(), 3, 1, 1, 0, 0, ght, gat)
		elif ght < gat:
			table.update_table(match.gethome(), 0, 1, 0, 1, 0, ght, gat)
		elif ght == gat:
			table.update_table(match.gethome(), 1, 1, 0, 0, 1, ght, gat)
		if ght > gat:
			table.update_table(match.getaway(), 0, 1, 0, 1, 0, gat, ght)
		elif ght < gat:
			table.update_table(match.getaway(), 3, 1, 1, 0, 0, gat, ght)
		elif ght == gat:
			table.update_table(match.getaway(), 1, 1, 0, 0, 1, gat, ght)
	table.display_table()
