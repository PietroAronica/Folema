import random
import copy
import itertools
import operator
import math
from bisect import bisect as _bisect
from itertools import repeat as _repeat
from datetime import date
import tabulate
import numpy as np
import Game as g
import Cup as cu

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

class CalendarDay(object):
	def __init__(self, month, week, midend, season):
		self.month = month
		self.week = week
		self.midend = midend
		self.id = month + '_' + str(week) + '_' + midend
		self.tabgames = {}
		self.othgames = {}
		self.grpgames = {}
		self.final = None
		self.season = season

	def add_league_games(self, league, games, table):
		self.tabgames[league.name] = {}
		self.tabgames[league.name]['games'] = games
		self.tabgames[league.name]['table'] = table

	def add_group_games(self, name, games, tables):
		self.grpgames['name'] = name
		self.grpgames['games'] = games
		self.grpgames['tables'] = tables

	def add_final(self, team1, team2):
		self.final = (team1, team2)

	def add_cup_games(self, roundname, games, action):
		self.othgames[roundname] = (action, games)

	def playday(self):
		for league in self.tabgames:
			day = self.tabgames[league]['games']
			table = self.tabgames[league]['table']
			for match in day.matches:
				result = g.auto_game(match.gethome(), match.getaway())
				team1 = match.gethome().getname()
				ght = result[0]
				gat = result[1]
				team2 = match.getaway().getname()
				if ght > gat:
					table.update_table(match.gethome(), 3, 1, 1, 0, 0, ght, gat, 'W')
				elif ght < gat:
					table.update_table(match.gethome(), 0, 1, 0, 1, 0, ght, gat, 'L')
				elif ght == gat:
					table.update_table(match.gethome(), 1, 1, 0, 0, 1, ght, gat, 'D')
				if ght > gat:
					table.update_table(match.getaway(), 0, 1, 0, 1, 0, gat, ght, 'L')
				elif ght < gat:
					table.update_table(match.getaway(), 3, 1, 1, 0, 0, gat, ght, 'W')
				elif ght == gat:
					table.update_table(match.getaway(), 1, 1, 0, 0, 1, gat, ght, 'D')
				match.gethome().calendar[day.get_num()] = [team2, ght, gat, 'H']
				match.getaway().calendar[day.get_num()] = [team1, gat, ght, 'A']
		for roundname in self.othgames:
			print(roundname)
			cup_results = self.othgames[roundname][0](self.othgames[roundname][1])
		if self.grpgames:
			cu.cupgameday_silent(self.grpgames['games'], self.grpgames['tables'])
		if self.final:
			print('Final')
			cup_results = cu.play_final(self.final[0], self.final[1])
		try:
			return cup_results
		except:
			pass

class Table(object):
	def __init__(self, teams):
		self.teams = {}
		self.teams_list = []
		for sq in teams:
			self.teams[sq.getname()] = [0,0,0,0,0,0,0,0," ",sq]
			self.teams_list.append(sq)

	def update_table(self, team, points, gamesplayed, gameswon, gameslost, gamesdrawn, goalsfor, goalsagainst, outcome):
		curr_points = self.teams[team.getname()][0]
		curr_gamesplayed = self.teams[team.getname()][1]
		curr_gameswon = self.teams[team.getname()][2]
		curr_gameslost = self.teams[team.getname()][3]
		curr_gamesdrawn = self.teams[team.getname()][4]
		curr_goalfor = self.teams[team.getname()][5]
		curr_goalagainst = self.teams[team.getname()][6]
		curr_goaldiff = self.teams[team.getname()][7]
		if self.teams[team.getname()][8] == ' ':
			curr_form = outcome
		else:
			curr_form = self.teams[team.getname()][8] + outcome
		if len(curr_form) > 5:
			curr_form = curr_form[1:]
		self.teams[team.getname()] = [curr_points+points,curr_gamesplayed+gamesplayed,curr_gameswon+gameswon,curr_gameslost+gameslost,curr_gamesdrawn+gamesdrawn,curr_goalfor+goalsfor,curr_goalagainst+goalsagainst,curr_goaldiff+(goalsfor-goalsagainst), curr_form, team]

	def get_position(self, team):
		sort_tab = sorted(sorted(sorted(sorted([[k] + v[:-1] for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True)
		positions = []
		for i in sort_tab:
			positions.append(i[0])
		return positions.index(team.getname()) + 1

	def get_team(self, position):
		sort_tab = sorted(sorted(sorted(sorted([[k] + v for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True)
		return sort_tab[position-1][10]

	def get_team_full_info(self, position):
		sort_tab = sorted(sorted(sorted(sorted([[k] + v for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True)
		return sort_tab[position-1][10]

	def display_table(self):
		headers = ["Position", "Team", "Points", "GP", "W", "L", "D", "GF", "GA", "Diff", "Recent Form"]
		print(tabulate.tabulate(sorted(sorted(sorted(sorted([[k] + v[:-1] for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True), headers = headers, showindex=range(1,len(self.teams)+1)))

class Team(object):
	def __init__(self, name, stats, conference, nation, league):
		self.name = name
		self.stats = {}
		self.stats['GK'] = float(stats[0])
		self.stats['DF'] = float(stats[1])
		self.stats['MD'] = float(stats[2])
		self.stats['AT'] = float(stats[3])
		self.stats['TP'] = float(stats[4])
		self.stats['FI'] = float(1)
		self.stats['MO'] = float(1)
		self.stats['PE'] = stats[5]
		self.history = {}
		self.history['Years'] = {}
		self.nation = nation
		self.league = league
		self.conference = conference

	def changestat(self, stat, value):
		self.stats[stat] = value

	def getname(self):
		return self.name

	def getstat(self, stat):
		return self.stats[stat]

	def getaverage(self):
		return round(np.average([self.stats['GK'], self.stats['DF'], self.stats['MD'], self.stats['AT'], self.stats['TP'], self.stats['FI'], self.stats['MO']]), 3)

	def getstats(self):
		return self.stats

	def set_calendar(self, calendar):
		self.calendar = calendar

	def getposition(self, table):
		return table.get_position(self)

	def getcalendar(self):
		for i in self.calendar:
			print(self.calendar[i])

	def yearrecord(self, year, league, position):
		try:
			self.history['Years'][year][league] = position
		except:
			self.history['Years'][year] = {}
			self.history['Years'][year][league] = position

class Match(object):
	def __init__(self, hometeam, awayteam):
		self.hometeam = hometeam
		self.awayteam = awayteam

	def gethome(self):
		return self.hometeam
	
	def getaway(self):
		return self.awayteam

	def getread(self):
		print('{:>30s}   -    {:<30s}'.format(self.gethome().getname(), self.getaway().getname()))

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
			match.getread()

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
			print(num)
			self.days[num].get_matches()

class League(object):
	def __init__(self, name, conference, nation, tier, rank):
		self.name = name
		self.conference = conference
		self.nation = nation
		self.tier = tier
		self.rank = rank
		self.teams = []
		self.promotesto = None
		self.relegatesto = None
		self.promotesfrom = None
		self.relegatesfrom = None

class Season(object):
	def __init__(self, year, leagueinfo):
		self.year = year
		self.calendar = {}
		for i in ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']:
			for t in [1,2,3,4]:
				for g in ['mid1', 'mid2', 'mid3', 'end']:
					self.calendar[i + '_' + str(t) + '_' + g] = CalendarDay(i,t,g, self)
		self.cupdays = {}
		self.cupinfo = {}
		self.tables = {}
		self.leagueinfo = leagueinfo
		self.champdays = {}
		for i in range(1,39):
			self.champdays[i] = {}

	def start_cups(self, prev_season):
		self.cupinfo['cmc'],  self.cupinfo['clc'] = cu.continental_cups_init(prev_season)
		c1 = cu.cup_matchmaker_1(self.cupinfo['cmc']['round one'])
		self.calendar['Jul_1_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 1 First Legs', c1, cu.first_legs)
		c1 = cu.cup_matchmaker_1(self.cupinfo['clc']['round one'])
		self.calendar['Jul_1_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 1 First Legs', c1, cu.first_legs)

	def add_table(self, league, teams):
		self.tables[league] = Table(teams)

	def add_champday(self, num, day, league):
		self.champdays[num][league] = day

	def run_season(self):
		for day in self.calendar:
			r = self.calendar[day].playday()
			if day == 'Jul_1_mid1':
				self.calendar['Jul_2_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 1 Second Legs', r, cu.second_legs)
			elif day == 'Jul_1_mid2':
				self.calendar['Jul_2_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 1 Second Legs', r, cu.second_legs)
			elif day == 'Jul_2_mid1':
				c2 = cu.cup_matchmaker_2(self.cupinfo['cmc']['round two'], r['winners'])
				self.cupinfo['clc']['round two'] = r['losers']
				self.calendar['Jul_4_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 2 First Legs', c2, cu.first_legs)
			elif day == 'Jul_2_mid2':
				c2 = cu.cup_matchmaker_2(self.cupinfo['clc']['round two'], r['winners'])
				self.calendar['Jul_4_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 2 First Legs', c2, cu.first_legs)
			elif day == 'Jul_4_mid1':
				self.calendar['Aug_1_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 2 Second Legs', r, cu.second_legs)
			elif day == 'Jul_4_mid2':
				self.calendar['Aug_1_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 2 Second Legs', r, cu.second_legs)
			elif day == 'Aug_1_mid1':
				r3_teams = []
				for t in self.cupinfo['cmc']['round three']:
					r3_teams.append(t)
				for t in r['winners']:
					r3_teams.append(t)
				c3 = cu.cup_matchmaker_3(r3_teams)
				self.calendar['Aug_3_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 3 First Legs', c3, cu.first_legs)
			elif day == 'Aug_1_mid2':
				r3_teams = []
				for t in self.cupinfo['clc']['round three']:
					r3_teams.append(t)
				for t in r['winners']:
					r3_teams.append(t)
				c3 = cu.cup_matchmaker_3(r3_teams)
				self.calendar['Aug_3_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 3 First Legs', c3, cu.first_legs)
			elif day == 'Aug_3_mid1':
				self.calendar['Aug_4_mid1'].add_cup_games('Continental Masters Cup Preliminary Round 3 Second Legs', r, cu.second_legs)
			elif day == 'Aug_3_mid2':
				self.calendar['Aug_4_mid2'].add_cup_games('Continental Challengers Cup Preliminary Round 3 Second Legs', r, cu.second_legs)
			elif day == 'Aug_4_mid1':
				for t in r['winners']:
					self.cupinfo['cmc']['group stage']['unsorted'].append(t)
				for t in r['losers']:
					self.cupinfo['clc']['group stage'].append(t)
				gs = cu.cup_groupmaker(self.cupinfo['cmc']['group stage'])
				self.cupinfo['cmc']['group stage tables'] = gs[2]
				self.calendar['Sep_3_mid1'].add_group_games('Continental Masters Cup Group Stage Day 1, Half 1', gs[1][1], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Sep_3_mid2'].add_group_games('Continental Masters Cup Group Stage Day 1, Half 2', gs[1][2], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Oct_1_mid1'].add_group_games('Continental Masters Cup Group Stage Day 2, Half 1', gs[1][3], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Oct_1_mid2'].add_group_games('Continental Masters Cup Group Stage Day 2, Half 2', gs[1][4], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Oct_3_mid1'].add_group_games('Continental Masters Cup Group Stage Day 3, Half 1', gs[1][5], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Oct_3_mid2'].add_group_games('Continental Masters Cup Group Stage Day 3, Half 2', gs[1][6], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Nov_1_mid1'].add_group_games('Continental Masters Cup Group Stage Day 4, Half 1', gs[1][7], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Nov_1_mid2'].add_group_games('Continental Masters Cup Group Stage Day 4, Half 2', gs[1][8], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Nov_3_mid1'].add_group_games('Continental Masters Cup Group Stage Day 5, Half 1', gs[1][9], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Nov_3_mid2'].add_group_games('Continental Masters Cup Group Stage Day 5, Half 2', gs[1][10], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Dec_1_mid1'].add_group_games('Continental Masters Cup Group Stage Day 6, Half 1', gs[1][11], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Dec_1_mid2'].add_group_games('Continental Masters Cup Group Stage Day 6, Half 2', gs[1][12], self.cupinfo['cmc']['group stage tables'])
			elif day == 'Aug_4_mid2':
				for t in r['winners']:
					self.cupinfo['clc']['group stage'].append(t)
				gs = cu.cup_groupmaker_1(self.cupinfo['clc']['group stage'])
				self.cupinfo['clc']['group stage tables'] = gs[2]
				self.calendar['Sep_3_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][1], self.cupinfo['clc']['group stage tables'])
				self.calendar['Oct_1_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][2], self.cupinfo['clc']['group stage tables'])
				self.calendar['Oct_3_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][3], self.cupinfo['clc']['group stage tables'])
				self.calendar['Nov_1_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][4], self.cupinfo['clc']['group stage tables'])
				self.calendar['Nov_3_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][5], self.cupinfo['clc']['group stage tables'])
				self.calendar['Dec_1_mid3'].add_group_games('Continental Challengers Cup Group Stage Day 1', gs[1][6], self.cupinfo['clc']['group stage tables'])
			elif day == 'Dec_1_mid2':
				r16 = cu.cup_matchmaker_4(self.cupinfo['cmc']['group stage tables'])
				self.calendar['Feb_2_mid1'].add_cup_games('Continental Masters Cup Round of 16, First Legs', r16, cu.first_legs)
			elif day == 'Dec_1_mid3':
				r32 = cu.cup_matchmaker_5(self.cupinfo['clc']['group stage tables'], self.cupinfo['cmc']['group stage tables'])
				self.calendar['Jan_2_mid3'].add_cup_games('Continental Challengers Cup Round of 32, First Legs', r32, cu.first_legs)
			elif day == 'Jan_2_mid3':
				self.calendar['Jan_3_mid3'].add_cup_games('Continental Challengers Cup Round of 32, Second Legs', r, cu.second_legs)
			elif day == 'Jan_3_mid3':
				r16 = cu.cup_matchmaker_1(r['winners'])
				self.calendar['Feb_2_mid3'].add_cup_games('Continental Challengers Cup Round of 16, First Legs', r16, cu.first_legs)
			elif day == 'Feb_2_mid1':
				self.calendar['Feb_3_mid1'].add_cup_games('Continental Masters Cup Round of 16, Second Legs', r, cu.second_legs)
			elif day == 'Feb_2_mid3':
				self.calendar['Feb_3_mid3'].add_cup_games('Continental Challengers Cup Round of 16, Second Legs', r, cu.second_legs)
			elif day == 'Feb_3_mid1':
				r8 = cu.cup_matchmaker_1(r['winners'])
				self.calendar['Mar_2_mid1'].add_cup_games('Continental Masters Cup Round of 8, First Legs', r8, cu.first_legs)
			elif day == 'Feb_3_mid3':
				r8 = cu.cup_matchmaker_1(r['winners'])
				self.calendar['Mar_2_mid3'].add_cup_games('Continental Challengers Cup Round of 8, First Legs', r8, cu.first_legs)
			elif day == 'Mar_2_mid1':
				self.calendar['Mar_3_mid1'].add_cup_games('Continental Masters Cup Round of 8, Second Legs', r, cu.second_legs)
			elif day == 'Mar_2_mid3':
				self.calendar['Mar_3_mid3'].add_cup_games('Continental Challengers Cup Round of 8, Second Legs', r, cu.second_legs)
			elif day == 'Mar_3_mid1':
				r4 = cu.cup_matchmaker_1(r['winners'])
				self.calendar['Apr_2_mid1'].add_cup_games('Continental Masters Cup Semifinals, First Legs', r4, cu.first_legs)
			elif day == 'Mar_3_mid3':
				r4 = cu.cup_matchmaker_1(r['winners'])
				self.calendar['Apr_2_mid3'].add_cup_games('Continental Challengers Cup Semifinals, First Legs', r4, cu.first_legs)
			elif day == 'Apr_2_mid1':
				self.calendar['Apr_3_mid1'].add_cup_games('Continental Masters Cup Semifinals, Second Legs', r, cu.second_legs)
			elif day == 'Apr_2_mid3':
				self.calendar['Apr_3_mid3'].add_cup_games('Continental Challengers Cup Semifinals, Second Legs', r, cu.second_legs)
			elif day == 'Apr_3_mid1':
				self.calendar['May_3_end'].add_final(r['winners'][0], r['winners'][1])
			elif day == 'Apr_3_mid3':
				self.calendar['May_3_mid3'].add_final(r['winners'][0], r['winners'][1])
			elif day == 'May_3_mid3':
				self.cupinfo['clc_winner'] = r[0]
			elif day == 'May_3_end':
				self.cupinfo['cmc_winner'] = r[0]

def make_new_season(season):
	year = int(season.year[:4])+1
	newyear = str(year) + '-' + str(year+1)[2:]
	newleagues = {}
	for league in season.leagueinfo:
		newleague = League(league, season.leagueinfo[league].conference, season.leagueinfo[league].nation, season.leagueinfo[league].tier, season.leagueinfo[league].rank)
		if season.leagueinfo[league].tier == 'T1' and season.leagueinfo[league].rank == 'R1':
			promfrom = season.leagueinfo[league].promotesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) <= 17:
					newleague.teams.append(team)
			for team in promfrom.teams:
				if season.tables[promfrom.name].get_position(team) <= 3:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T1' and season.leagueinfo[league].rank == 'R2':
			promfrom = season.leagueinfo[league].promotesfrom
			relefrom = season.leagueinfo[league].relegatesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) <= 17 and season.tables[league].get_position(team) >= 4:
					newleague.teams.append(team)
			for team in promfrom.teams:
				if season.tables[promfrom.name].get_position(team) <= 3:
					newleague.teams.append(team)
					team.league = newleague
			for team in relefrom.teams:
				if season.tables[relefrom.name].get_position(team) >= 18:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T1' and season.leagueinfo[league].rank == 'R3':
			relefrom = season.leagueinfo[league].relegatesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) >= 4:
					newleague.teams.append(team)
			for team in relefrom.teams:
				if season.tables[relefrom.name].get_position(team) >= 18:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T2' and season.leagueinfo[league].rank == 'R1':
			promfrom = season.leagueinfo[league].promotesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) <= 17:
					newleague.teams.append(team)
			for team in promfrom.teams:
				if season.tables[promfrom.name].get_position(team) <= 3:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T2' and season.leagueinfo[league].rank == 'R2':
			relefrom = season.leagueinfo[league].relegatesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) >= 4:
					newleague.teams.append(team)
			for team in relefrom.teams:
				if season.tables[relefrom.name].get_position(team) >= 18:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T3' and season.leagueinfo[league].rank == 'R1':
			promfrom = season.leagueinfo[league].promotesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) <= 8:
					newleague.teams.append(team)
			for team in promfrom.teams:
				if season.tables[promfrom.name].get_position(team) <= 2:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T3' and season.leagueinfo[league].rank == 'R2':
			relefrom = season.leagueinfo[league].relegatesfrom
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				if season.tables[league].get_position(team) >= 3:
					newleague.teams.append(team)
			for team in relefrom.teams:
				if season.tables[relefrom.name].get_position(team) >= 9:
					newleague.teams.append(team)
					team.league = newleague
		elif season.leagueinfo[league].tier == 'T4':
			for team in season.leagueinfo[league].teams:
				team.yearrecord(season.year, league, season.tables[league].get_position(team))
				newleague.teams.append(team)
		newleagues[league] = newleague
	newseason = Season(newyear, newleagues)
	for l in newleagues:
		newseason.add_table(l, newleagues[l].teams)
		y = makecalendar(newleagues[l].teams)
		if len(newseason.leagueinfo[l].teams) == 20:
			newseason.calendar['Aug_3_end'].add_league_games(newleagues[l], y.days[1], newseason.tables[l])
			newseason.calendar['Aug_4_end'].add_league_games(newleagues[l], y.days[2], newseason.tables[l])
			newseason.calendar['Sep_1_end'].add_league_games(newleagues[l], y.days[3], newseason.tables[l])
			newseason.calendar['Sep_2_end'].add_league_games(newleagues[l], y.days[4], newseason.tables[l])
			newseason.calendar['Sep_3_end'].add_league_games(newleagues[l], y.days[5], newseason.tables[l])
			newseason.calendar['Sep_4_end'].add_league_games(newleagues[l], y.days[6], newseason.tables[l])
			newseason.calendar['Oct_1_end'].add_league_games(newleagues[l], y.days[7], newseason.tables[l])
			newseason.calendar['Oct_2_mid3'].add_league_games(newleagues[l], y.days[8], newseason.tables[l])
			newseason.calendar['Oct_2_end'].add_league_games(newleagues[l], y.days[9], newseason.tables[l])
			newseason.calendar['Oct_3_end'].add_league_games(newleagues[l], y.days[10], newseason.tables[l])
			newseason.calendar['Oct_4_end'].add_league_games(newleagues[l], y.days[11], newseason.tables[l])
			newseason.calendar['Nov_1_end'].add_league_games(newleagues[l], y.days[12], newseason.tables[l])
			newseason.calendar['Nov_2_end'].add_league_games(newleagues[l], y.days[13], newseason.tables[l])
			newseason.calendar['Nov_3_end'].add_league_games(newleagues[l], y.days[14], newseason.tables[l])
			newseason.calendar['Nov_4_mid3'].add_league_games(newleagues[l], y.days[15], newseason.tables[l])
			newseason.calendar['Nov_4_end'].add_league_games(newleagues[l], y.days[16], newseason.tables[l])
			newseason.calendar['Dec_1_end'].add_league_games(newleagues[l], y.days[17], newseason.tables[l])
			newseason.calendar['Dec_2_end'].add_league_games(newleagues[l], y.days[18], newseason.tables[l])
			newseason.calendar['Dec_3_end'].add_league_games(newleagues[l], y.days[19], newseason.tables[l])
			newseason.calendar['Jan_2_end'].add_league_games(newleagues[l], y.days[20], newseason.tables[l])
			newseason.calendar['Jan_3_mid3'].add_league_games(newleagues[l], y.days[21], newseason.tables[l])
			newseason.calendar['Jan_3_end'].add_league_games(newleagues[l], y.days[22], newseason.tables[l])
			newseason.calendar['Jan_4_end'].add_league_games(newleagues[l], y.days[23], newseason.tables[l])
			newseason.calendar['Feb_1_end'].add_league_games(newleagues[l], y.days[24], newseason.tables[l])
			newseason.calendar['Feb_2_end'].add_league_games(newleagues[l], y.days[25], newseason.tables[l])
			newseason.calendar['Feb_3_end'].add_league_games(newleagues[l], y.days[26], newseason.tables[l])
			newseason.calendar['Feb_4_end'].add_league_games(newleagues[l], y.days[27], newseason.tables[l])
			newseason.calendar['Mar_1_mid3'].add_league_games(newleagues[l], y.days[28], newseason.tables[l])
			newseason.calendar['Mar_1_end'].add_league_games(newleagues[l], y.days[29], newseason.tables[l])
			newseason.calendar['Mar_2_end'].add_league_games(newleagues[l], y.days[30], newseason.tables[l])
			newseason.calendar['Mar_3_end'].add_league_games(newleagues[l], y.days[31], newseason.tables[l])
			newseason.calendar['Mar_4_end'].add_league_games(newleagues[l], y.days[32], newseason.tables[l])
			newseason.calendar['Apr_1_mid3'].add_league_games(newleagues[l], y.days[33], newseason.tables[l])
			newseason.calendar['Apr_1_end'].add_league_games(newleagues[l], y.days[34], newseason.tables[l])
			newseason.calendar['Apr_2_end'].add_league_games(newleagues[l], y.days[35], newseason.tables[l])
			newseason.calendar['Apr_3_end'].add_league_games(newleagues[l], y.days[36], newseason.tables[l])
			newseason.calendar['Apr_4_end'].add_league_games(newleagues[l], y.days[37], newseason.tables[l])
			newseason.calendar['May_1_end'].add_league_games(newleagues[l], y.days[38], newseason.tables[l])
		elif len(newseason.leagueinfo[l].teams) == 10:
			newseason.calendar['Aug_4_end'].add_league_games(newleagues[l], y.days[1], newseason.tables[l])
			newseason.calendar['Sep_2_end'].add_league_games(newleagues[l], y.days[2], newseason.tables[l])
			newseason.calendar['Sep_4_end'].add_league_games(newleagues[l], y.days[3], newseason.tables[l])
			newseason.calendar['Oct_2_end'].add_league_games(newleagues[l], y.days[4], newseason.tables[l])
			newseason.calendar['Oct_4_end'].add_league_games(newleagues[l], y.days[5], newseason.tables[l])
			newseason.calendar['Nov_2_end'].add_league_games(newleagues[l], y.days[6], newseason.tables[l])
			newseason.calendar['Nov_4_end'].add_league_games(newleagues[l], y.days[7], newseason.tables[l])
			newseason.calendar['Dec_2_end'].add_league_games(newleagues[l], y.days[8], newseason.tables[l])
			newseason.calendar['Dec_3_end'].add_league_games(newleagues[l], y.days[9], newseason.tables[l])
			newseason.calendar['Jan_2_end'].add_league_games(newleagues[l], y.days[10], newseason.tables[l])
			newseason.calendar['Jan_4_end'].add_league_games(newleagues[l], y.days[11], newseason.tables[l])
			newseason.calendar['Feb_2_end'].add_league_games(newleagues[l], y.days[12], newseason.tables[l])
			newseason.calendar['Feb_4_end'].add_league_games(newleagues[l], y.days[13], newseason.tables[l])
			newseason.calendar['Mar_2_end'].add_league_games(newleagues[l], y.days[14], newseason.tables[l])
			newseason.calendar['Mar_4_end'].add_league_games(newleagues[l], y.days[15], newseason.tables[l])
			newseason.calendar['Apr_2_end'].add_league_games(newleagues[l], y.days[16], newseason.tables[l])
			newseason.calendar['Apr_4_end'].add_league_games(newleagues[l], y.days[17], newseason.tables[l])
			newseason.calendar['May_1_end'].add_league_games(newleagues[l], y.days[18], newseason.tables[l])
	for l in newleagues:
		if newleagues[l].tier == 'T1' and newleagues[l].rank == 'R1':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R2':
					newleagues[l].relegatesto = newleagues[l2]
					newleagues[l].promotesfrom = newleagues[l2]
		if newleagues[l].tier == 'T1' and newleagues[l].rank == 'R2':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R1':
					newleagues[l].promotesto = newleagues[l2]
					newleagues[l].relegatesfrom = newleagues[l2]
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R3':
					newleagues[l].relegatesto = newleagues[l2]
					newleagues[l].promotesfrom = newleagues[l2]
		if newleagues[l].tier == 'T1' and newleagues[l].rank == 'R3':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R2':
					newleagues[l].promotesto = newleagues[l2]
					newleagues[l].relegatesfrom = newleagues[l2]
		if newleagues[l].tier == 'T2' and newleagues[l].rank == 'R1':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R2':
					newleagues[l].relegatesto = newleagues[l2]
					newleagues[l].promotesfrom = newleagues[l2]
		if newleagues[l].tier == 'T2' and newleagues[l].rank == 'R2':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R1':
					newleagues[l].promotesto = newleagues[l2]
					newleagues[l].relegatesfrom = newleagues[l2]
		if newleagues[l].tier == 'T3' and newleagues[l].rank == 'R1':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R2':
					newleagues[l].relegatesto = newleagues[l2]
					newleagues[l].promotesfrom = newleagues[l2]
		if newleagues[l].tier == 'T3' and newleagues[l].rank == 'R2':
			for l2 in newleagues:
				if newleagues[l2].nation == newleagues[l].nation and newleagues[l2].rank == 'R1':
					newleagues[l].promotesto = newleagues[l2]
					newleagues[l].relegatesfrom = newleagues[l2]
	return newseason
					
def maketeam(name, n):
	team = Team(name, [n,n,n,n,n,n],'C', 'N', 'L')
	return team
def maketeam_perfect(name):
	team = Team(name, [1,1,1,1,1])
	return team
def maketeam_strong(name):
	team = Team(name, [0.8,0.8,0.8,0.8,0.8,0.8],'C', 'N', 'L')
	return team
def maketeam_mid(name):
	team = Team(name, [0.5,0.5,0.5,0.5,0.5])
	return team
def maketeam_weak(name):
	team = Team(name, [0.2,0.2,0.2,0.2,0.2])
	return team

def pairwise(items):
	a = iter(items)
	return zip(a, a)

def makeleague(inputfile):
	dataset = []
	f = open(inputfile)
	opened = f.readlines()
	for line in opened:
		name,stats = line.split('=')
		vals = []
		for num in stats.split(','):
			vals.append(num.strip())
		dataset.append(Team(name.strip(),vals))
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
	matchdays = list(range(1,len(league)))
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
	for team in league:
		cale = {}
		for d in year.days:
			for m in year.days[d].matches:
				if m.gethome() == team:
					cale[d] = [m.getaway().getname(), 'H']
				elif m.getaway() == team:
					cale[d] = [m.gethome().getname(), 'A']
		team.set_calendar(cale)
	return year

def gameday(day, table):
	for match in day.matches:
		result = g.auto_game(match.gethome(), match.getaway())
		team1 = match.gethome().getname()
		ght = result[0]
		gat = result[1]
		team2 = match.getaway().getname()
		print('{:>30s} {:2} {:2}  {:<30s}'.format(team1, ght, gat, team2))
		if ght > gat:
			table.update_table(match.gethome(), 3, 1, 1, 0, 0, ght, gat, 'W')
		elif ght < gat:
			table.update_table(match.gethome(), 0, 1, 0, 1, 0, ght, gat, 'L')
		elif ght == gat:
			table.update_table(match.gethome(), 1, 1, 0, 0, 1, ght, gat, 'D')
		if ght > gat:
			table.update_table(match.getaway(), 0, 1, 0, 1, 0, gat, ght, 'L')
		elif ght < gat:
			table.update_table(match.getaway(), 3, 1, 1, 0, 0, gat, ght, 'W')
		elif ght == gat:
			table.update_table(match.getaway(), 1, 1, 0, 0, 1, gat, ght, 'D')
		match.gethome().calendar[day.get_num()] = [team2, ght, gat, 'H']
		match.getaway().calendar[day.get_num()] = [team1, gat, ght, 'A']
	table.display_table()

def season_gameday(season, num):
	for league in season.champdays[num]:
		day = season.champdays[num][league]
		table = season.tables[league]
		for match in day.matches:
			result = g.auto_game(match.gethome(), match.getaway())
			team1 = match.gethome().getname()
			ght = result[0]
			gat = result[1]
			team2 = match.getaway().getname()
			if ght > gat:
				table.update_table(match.gethome(), 3, 1, 1, 0, 0, ght, gat, 'W')
			elif ght < gat:
				table.update_table(match.gethome(), 0, 1, 0, 1, 0, ght, gat, 'L')
			elif ght == gat:
				table.update_table(match.gethome(), 1, 1, 0, 0, 1, ght, gat, 'D')
			if ght > gat:
				table.update_table(match.getaway(), 0, 1, 0, 1, 0, gat, ght, 'L')
			elif ght < gat:
				table.update_table(match.getaway(), 3, 1, 1, 0, 0, gat, ght, 'W')
			elif ght == gat:
				table.update_table(match.getaway(), 1, 1, 0, 0, 1, gat, ght, 'D')
			match.gethome().calendar[day.get_num()] = [team2, ght, gat, 'H']
			match.getaway().calendar[day.get_num()] = [team1, gat, ght, 'A']

def postmatch(team):
	fi = team.getstat('FI')
	gap = 1-fi
	team.changestat('FI', fi+gap*choices([0.20,0.30,0.40,0.50,0.60,0.70], weights=[10,15,30,25,15,5])[0])
	fi = team.getstat('FI')
	if fi > 1:
		team.changestat('FI', 1)
	elif fi <= 0:
		team.changestat('FI', 0.01)
		

def playyear(year, table):
	for day in year.days:
		gameday(year.days[day], table)
		for team in table.teams_list:
			postmatch(team)
		input("Press Enter to continue:")

def playyear_interactive(year, table, team):
	print("You are playing as " + team.getname() + ".")
	for day in year.days:
		print("This is day " + str(day) + ".")
		gameday_interactive(year.days[day], table, team)
		for squad in table.teams_list:
			postmatch(squad)
		input("Press Enter to continue:")

def start_season():
	infile = open('Leagues.dat')
	opened = infile.readlines() 
	leagues = {}
	for line in opened:
		curr_league = line.split(',')[4].strip()
		if curr_league not in leagues:
			leagues[curr_league] = League(curr_league, line.split(',')[0].strip(), line.split(',')[1].strip(), line.split(',')[2].strip(), line.split(',')[3].strip())
		if leagues[curr_league].tier == 'T1' and leagues[curr_league].rank == 'R1':
			distval = ([6,7,8,9],[5,30,50,15])
		elif leagues[curr_league].tier == 'T1' and leagues[curr_league].rank == 'R2':
			distval = ([4,5,6,7],[10,15,60,15])
		elif leagues[curr_league].tier == 'T1' and leagues[curr_league].rank == 'R3':
			distval = ([2,3,4,5],[10,20,70,20])
		elif leagues[curr_league].tier == 'T2' and leagues[curr_league].rank == 'R1':
			distval = ([5,6,7,8,9],[10,35,45,9,1])
		elif leagues[curr_league].tier == 'T2' and leagues[curr_league].rank == 'R2':
			distval = ([2,3,4,5,6],[2,8,50,35,5])
		elif leagues[curr_league].tier == 'T3' and leagues[curr_league].rank == 'R1':
			distval = ([4,5,6],[20,50,30])
		elif leagues[curr_league].tier == 'T3' and leagues[curr_league].rank == 'R2':
			distval = ([2,3,4],[10,50,40])
		elif leagues[curr_league].tier == 'T4' and leagues[curr_league].rank == 'R1':
			distval = ([1,2,3,4],[25,40,30,5])
		ov = choices(distval[0], weights=distval[1])[0]
		vals = []
		for z in range(5):
			vals.append((ov*10-random.randrange(-6,6))/float(100))
		vals.append(choices(['Pragmatic', 'Aggressive', 'Cautious', 'Unambitious'], weights=[35,25,25,15])[0])
		leagues[curr_league].teams.append(Team(line.split(',')[5].strip(),vals,line.split(',')[0].strip(), line.split(',')[1].strip(),leagues[curr_league]))
	infile.close()
	for l in leagues:
		if leagues[l].tier == 'T1' and leagues[l].rank == 'R1':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R2':
					leagues[l].relegatesto = leagues[l2]
					leagues[l].promotesfrom = leagues[l2]
		if leagues[l].tier == 'T1' and leagues[l].rank == 'R2':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R1':
					leagues[l].promotesto = leagues[l2]
					leagues[l].relegatesfrom = leagues[l2]
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R3':
					leagues[l].relegatesto = leagues[l2]
					leagues[l].promotesfrom = leagues[l2]
		if leagues[l].tier == 'T1' and leagues[l].rank == 'R3':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R2':
					leagues[l].promotesto = leagues[l2]
					leagues[l].relegatesfrom = leagues[l2]
		if leagues[l].tier == 'T2' and leagues[l].rank == 'R1':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R2':
					leagues[l].relegatesto = leagues[l2]
					leagues[l].promotesfrom = leagues[l2]
		if leagues[l].tier == 'T2' and leagues[l].rank == 'R2':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R1':
					leagues[l].promotesto = leagues[l2]
					leagues[l].relegatesfrom = leagues[l2]
		if leagues[l].tier == 'T3' and leagues[l].rank == 'R1':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R2':
					leagues[l].relegatesto = leagues[l2]
					leagues[l].promotesfrom = leagues[l2]
		if leagues[l].tier == 'T3' and leagues[l].rank == 'R2':
			for l2 in leagues:
				if leagues[l2].nation == leagues[l].nation and leagues[l2].rank == 'R1':
					leagues[l].promotesto = leagues[l2]
					leagues[l].relegatesfrom = leagues[l2]
	cy = date.today().year - 2
	year = str(cy) + '-' + str(cy+1)[2:]
	season = Season(year, leagues)
	for l in leagues:
		y = makecalendar(leagues[l].teams)
		if leagues[l].tier in ['T1', 'T2']:
			for d in y.days:
				season.add_champday(d, y.days[d], l)
		elif leagues[l].tier in ['T3', 'T4']:
			for d in y.days:
				season.add_champday(d*2, y.days[d], l)
		season.add_table(l, leagues[l].teams)
	for i in range(1,39):
		season_gameday(season, i)
	n_season = make_new_season(season)
	leagues = n_season.leagueinfo
	for l in leagues:
		y = makecalendar(leagues[l].teams)
		if leagues[l].tier in ['T1', 'T2']:
			for d in y.days:
				n_season.add_champday(d, y.days[d], l)
		elif leagues[l].tier in ['T3', 'T4']:
			for d in y.days:
				n_season.add_champday(d*2, y.days[d], l)
		n_season.add_table(l, leagues[l].teams)
	i_l = {}
	i_l['round three'] = []
	i_m = {}
	i_m['round one'] = []
	i_m['round two'] = []
	i_m['round three'] = []
	for league in season.leagueinfo:
		if season.leagueinfo[league].tier == "T4" and season.leagueinfo[league].conference == 'Europe':
			i_m['round one'].append(season.tables[league].get_team(1))
		elif season.leagueinfo[league].tier == "T3" and season.leagueinfo[league].rank == "R1" and season.leagueinfo[league].conference == 'Europe':
			i_m['round two'].append(season.tables[league].get_team(1))
			i_l['round three'].append(season.tables[league].get_team(2))
		elif season.leagueinfo[league].tier == "T2" and season.leagueinfo[league].rank == "R1" and season.leagueinfo[league].conference == 'Europe':
			i_m['round three'].append(season.tables[league].get_team(1))
			i_m['round three'].append(season.tables[league].get_team(2))
			i_l['round three'].append(season.tables[league].get_team(3))
			i_l['round three'].append(season.tables[league].get_team(4))
		elif season.leagueinfo[league].tier == "T1" and season.leagueinfo[league].rank == "R1" and season.leagueinfo[league].conference == 'Europe':
			i_m['round three'].append(season.tables[league].get_team(1))
			i_m['round three'].append(season.tables[league].get_team(2))
			i_m['round three'].append(season.tables[league].get_team(3))
			i_l['round three'].append(season.tables[league].get_team(4))
	r1 = cu.cup_matchmaker_1(i_m['round one'])
	r11 = cu.first_legs_silent(r1)
	r12 = cu.second_legs_silent(r11)
	r2 = cu.cup_matchmaker_2(i_m['round two'], r12['winners'])
	r21 = cu.first_legs_silent(r2)
	r22 = cu.second_legs_silent(r21)
	i_m['round three'].extend(r22['winners'])
	r3 = cu.cup_matchmaker_3(i_m['round three'])
	r31 = cu.first_legs_silent(r3)
	r32 = cu.second_legs_silent(r31)
	r16 = cu.cup_matchmaker_6(r32['winners'])
	r161 = cu.first_legs_silent(r16)
	r162 = cu.second_legs_silent(r161)
	r8 = cu.cup_matchmaker_1(r162['winners'])
	r81 = cu.first_legs_silent(r8)
	r82 = cu.second_legs_silent(r81)
	r4 = cu.cup_matchmaker_1(r82['winners'])
	r41 = cu.first_legs_silent(r4)
	r42 = cu.second_legs_silent(r41)
	n_season.cupinfo['cmc_winner'] = cu.play_final_silent(r42['winners'][0], r42['winners'][1])[0]
	i_l['round three'].extend(r22['losers'])
	r3 = cu.cup_matchmaker_3(i_l['round three'])
	r31 = cu.first_legs_silent(r3)
	r32 = cu.second_legs_silent(r31)
	r16 = cu.cup_matchmaker_6(r32['winners'])
	r161 = cu.first_legs_silent(r16)
	r162 = cu.second_legs_silent(r161)
	r8 = cu.cup_matchmaker_1(r162['winners'])
	r81 = cu.first_legs_silent(r8)
	r82 = cu.second_legs_silent(r81)
	r4 = cu.cup_matchmaker_1(r82['winners'])
	r41 = cu.first_legs_silent(r4)
	r42 = cu.second_legs_silent(r41)
	n_season.cupinfo['clc_winner'] = cu.play_final_silent(r42['winners'][0], r42['winners'][1])[0]
	for i in range(1,39):
		season_gameday(n_season, i)
	season = make_new_season(n_season)
	season.start_cups(n_season)
	return season
