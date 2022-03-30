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
import Champyonship as cp

nation_flags = {'England':'\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F','Italy':'\U0001F1EE\U0001F1F9','Germany':'\U0001F1E9\U0001F1EA','Spain':'\U0001F1EA\U0001F1F8','France':'\U0001F1EB\U0001F1F7','Portugal':'\U0001F1F5\U0001F1F9','Russia':'\U0001F1F7\U0001F1FA','Netherlands':'\U0001F1F3\U0001F1F1', 'Scotland':'\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F', 'Ukraine':'\U0001F1FA\U0001F1E6', 'Belgium':'\U0001F1E7\U0001F1EA', 'Ireland':'\U0001F1EE\U0001F1EA','Poland':'\U0001F1F5\U0001F1F1'}
#nation_flags = {'England':'\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F','Italy':'\U000fe4e9','Germany':'\U000FE4E8','Spain':'\U000FE4EB','France':'\U000FE4E7','Portugal':'\U0001F1F5\U0001F1F9','Russia':'\U000fe4ec','Netherlands':'\U0001F1F3\U0001F1F1', 'Scotland':'\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F', 'Ukraine':'\U0001F1FA\U0001F1E6', 'Belgium':'\U0001F1E7\U0001F1EA', 'Ireland':'\U0001F1EE\U0001F1EA','Poland':'\U0001F1F5\U0001F1F1'}

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

class CupDay(object):
	def __init__(self, number):
		self.number = number
		self.matches = {}

	def get_num(self):
		return self.number
	
	def get_matches(self):
		for group in self.matches:
			print('Group ' + str(group))
			for match in self.matches[group]:
				match.getread()

	def add_match(self, group, match):
		try:
			self.matches[group].append(match)
		except:
			self.matches[group] = []
			self.matches[group].append(match)

def cupgameday(day, tables):
	for gr in day.matches:
		table = tables[gr]
		for match in day.matches[gr]:
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

def cupgameday_silent(day, tables):
	for gr in day.matches:
		table = tables[gr]
		for match in day.matches[gr]:
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

def continental_cups_init(prev_season):
	cmc_rounds = {}
	cmc_rounds['round one'] = []
	cmc_rounds['round two'] = []
	cmc_rounds['round three'] = []
	cmc_rounds['group stage'] = {}
	cmc_rounds['group stage']['pot one'] = []
	cmc_rounds['group stage']['unsorted'] = []
	clc_rounds = {}
	clc_rounds['round one'] = []
	clc_rounds['round two'] = []
	clc_rounds['round three'] = []
	clc_rounds['group stage'] = []
	cmc_winner = prev_season.cupinfo['cmc_winner']
	clc_winner = prev_season.cupinfo['clc_winner']
	cmc_rounds['group stage']['pot one'].append(cmc_winner)
	cmc_rounds['group stage']['pot one'].append(clc_winner)
	coin = [0,0]
	for league in prev_season.leagueinfo:
		if prev_season.leagueinfo[league].tier == "T4" and prev_season.leagueinfo[league].conference == 'Europe':
			n = [1,2,3,4]
			if cmc_winner.league.name == league and prev_season.tables[league].get_position(cmc_winner) in [1,2]:
				n.remove(prev_season.tables[league].get_position(cmc_winner))
			if clc_winner.league.name == league and prev_season.tables[league].get_position(clc_winner) in [1,2]:
				n.remove(prev_season.tables[league].get_position(clc_winner))
			cmc_rounds['round one'].append(prev_season.tables[league].get_team(n[0]))
			clc_rounds['round one'].append(prev_season.tables[league].get_team(n[1]))
		elif prev_season.leagueinfo[league].tier == "T3" and prev_season.leagueinfo[league].rank == "R1" and prev_season.leagueinfo[league].conference == 'Europe':
			n = [1,2,3,4,5]
			if cmc_winner.league.name == league and prev_season.tables[league].get_position(cmc_winner) in [1,2,3]:
				n.remove(prev_season.tables[league].get_position(cmc_winner))
			if clc_winner.league.name == league and prev_season.tables[league].get_position(clc_winner) in [1,2,3]:
				n.remove(prev_season.tables[league].get_position(clc_winner))
			cmc_rounds['round three'].append(prev_season.tables[league].get_team(n[0]))
			cmc_rounds['round two'].append(prev_season.tables[league].get_team(n[1]))
			clc_rounds['round three'].append(prev_season.tables[league].get_team(n[2]))
		elif prev_season.leagueinfo[league].tier == "T2" and prev_season.leagueinfo[league].rank == "R1" and prev_season.leagueinfo[league].conference == 'Europe':
			n = [1,2,3,4,5,6,7,8]
			if cmc_winner.league.name == league and prev_season.tables[league].get_position(cmc_winner) in [1,2,3,4,5,6]:
				n.remove(prev_season.tables[league].get_position(cmc_winner))
			if clc_winner.league.name == league and prev_season.tables[league].get_position(clc_winner) in [1,2,3,4,5,6]:
				n.remove(prev_season.tables[league].get_position(clc_winner))
			coin_flip = random.randrange(2)
			if coin_flip == 1 and coin[0] < 2:
				cmc_rounds['group stage']['pot one'].append(prev_season.tables[league].get_team(n[0]))
				coin[0]+=1
				coin[1]+=1
			elif coin[1] >= 2 and coin[0] < 1:
				cmc_rounds['group stage']['pot one'].append(prev_season.tables[league].get_team(n[0]))
				coin[0]+=1
				coin[1]+=1
			elif coin[1] >= 3 and coin[0] < 2:
				cmc_rounds['group stage']['pot one'].append(prev_season.tables[league].get_team(n[0]))
				coin[0]+=1
				coin[1]+=1
			else:
				cmc_rounds['group stage']['unsorted'].append(prev_season.tables[league].get_team(n[0]))
				coin[1]+=1
			cmc_rounds['round three'].append(prev_season.tables[league].get_team(n[1]))
			cmc_rounds['round three'].append(prev_season.tables[league].get_team(n[2]))
			clc_rounds['group stage'].append(prev_season.tables[league].get_team(n[3]))
			clc_rounds['round three'].append(prev_season.tables[league].get_team(n[4]))
			clc_rounds['round three'].append(prev_season.tables[league].get_team(n[5]))
		elif prev_season.leagueinfo[league].tier == "T1" and prev_season.leagueinfo[league].rank == "R1" and prev_season.leagueinfo[league].conference == 'Europe':
			n = [1,2,3,4,5,6,7,8]
			if cmc_winner.league.name == league and prev_season.tables[league].get_position(cmc_winner) in [1,2,3,4,5,6]:
				n.remove(prev_season.tables[league].get_position(cmc_winner))
			if clc_winner.league.name == league and prev_season.tables[league].get_position(clc_winner) in [1,2,3,4,5,6]:
				n.remove(prev_season.tables[league].get_position(clc_winner))
			cmc_rounds['group stage']['pot one'].append(prev_season.tables[league].get_team(n[0]))
			cmc_rounds['group stage']['unsorted'].append(prev_season.tables[league].get_team(n[1]))
			cmc_rounds['round three'].append(prev_season.tables[league].get_team(n[2]))
			clc_rounds['group stage'].append(prev_season.tables[league].get_team(n[3]))
			clc_rounds['group stage'].append(prev_season.tables[league].get_team(n[4]))
			clc_rounds['round three'].append(prev_season.tables[league].get_team(n[5]))
	return cmc_rounds, clc_rounds

def cup_matchmaker_1(teams):
	matches = []
	for i in range(int(len(teams)/2)):
		t1 = random.choice(teams)
		teams.remove(t1)
		t2 = random.choice(teams)
		teams.remove(t2)
		matches.append(cp.Match(t1,t2))
	return matches

def cup_matchmaker_2(seeded_teams, unseeded_teams):
	matches = []
	for i in range(len(seeded_teams)):
		t1 = random.choice(seeded_teams)
		seeded_teams.remove(t1)
		t2 = random.choice(unseeded_teams)
		unseeded_teams.remove(t2)
		matches.append(cp.Match(t1,t2))
	return matches

def cup_matchmaker_3(teams):
	matches = []
	seeded_teams = []
	unseeded_teams = []
	n = len(teams)
	t1 = []
	t2 = []
	t3 = []
	t4 = []
	nations = {}
	for t in teams:
		if t.league.tier == 'T1':
			t1.append(t)
		elif t.league.tier == 'T2':
			t2.append(t)
		elif t.league.tier == 'T3':
			t3.append(t)
		elif t.league.tier == 'T4':
			t4.append(t)
		try:
			nations[t.nation]+=1
		except:
			nations[t.nation]=1
	while len(t1) > 0 and len(seeded_teams) < int(n/2):
		t = random.choice(t1)
		seeded_teams.append(t)
		t1.remove(t)
	while len(t2) > 0 and len(seeded_teams) < int(n/2):
		t = random.choice(t2)
		seeded_teams.append(t)
		t2.remove(t)
	while len(t3) > 0 and len(seeded_teams) < int(n/2):
		t = random.choice(t3)
		seeded_teams.append(t)
		t3.remove(t)
	while len(t4) > 0 and len(seeded_teams) < int(n/2):
		t = random.choice(t4)
		seeded_teams.append(t)
		t4.remove(t)
	while len(t1) > 0:
		t = random.choice(t1)
		unseeded_teams.append(t)
		t1.remove(t)
	while len(t2) > 0:
		t = random.choice(t2)
		unseeded_teams.append(t)
		t2.remove(t)
	while len(t3) > 0:
		t = random.choice(t3)
		unseeded_teams.append(t)
		t3.remove(t)
	while len(t4) > 0:
		t = random.choice(t4)
		unseeded_teams.append(t)
		t4.remove(t)
	rank_n = sorted(nations.items(), key=operator.itemgetter(1))
	mpn = rank_n[-1][1]
	if mpn > int(n/2):
		while len(seeded_teams) > 0:
			t1 = random.choice(seeded_teams)
			seeded_teams.remove(t1)
			t2 = random.choice(unseeded_teams)
			unseeded_teams.remove(t2)
			matches.append(cp.Match(t1,t2))
	else:
		redo = 'y'
		while redo == 'y':
			matches = []
			redo = 'n'
#			prin = 'n'
			st = copy.deepcopy(seeded_teams)
			ut = copy.deepcopy(unseeded_teams)
			while len(st) > 0:
				t1 = random.choice(st)
				st.remove(t1)
				t2 = random.choice(ut)
				ut.remove(t2)
				matches.append(cp.Match(t1,t2))
			for m in matches:
				if m.gethome().nation == m.getaway().nation:
#					prin = 'y'
					redo = 'y'
#			for m in matches:
#				if prin == 'y':
#					m.getread()
	return matches

def cup_matchmaker_4(tables):
	nextround = {}
	nextround['seeded'] = []
	nextround['unseeded'] = []
	for i in tables:
		nextround['seeded'].append((tables[i].get_team(1), i))
		nextround['unseeded'].append((tables[i].get_team(2), i))
	redo = 'y'
	while redo == 'y':
		nround = []
		redo = 'n'
		us = copy.deepcopy(nextround['unseeded'])
		for seed in nextround['seeded']:
			t = seed[0]
			temp = []
			for unseed in us:
				if unseed[1] != seed[1] and t.nation != unseed[0].nation:
					temp.append(unseed)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t2 = random.choice(temp)
				nround.append(cp.Match(t2[0], t))
				us.remove(t2)
	return nround

def cup_matchmaker_5(tables, tables2):
	demoted = []
	for i in tables2:
		demoted.append(tables2[i].get_team(3))
	temptable = cp.Table(demoted)
	for i in range(len(tables2)):
		temptable.update_table(demoted[i], tables2[i+1].teams[demoted[i].name][0], tables2[i+1].teams[demoted[i].name][1], tables2[i+1].teams[demoted[i].name][2], tables2[i+1].teams[demoted[i].name][3], tables2[i+1].teams[demoted[i].name][4], tables2[i+1].teams[demoted[i].name][5], tables2[i+1].teams[demoted[i].name][6], 'X')
	nextround = {}
	nextround['seeded'] = []
	nextround['unseeded'] = []
	for i in tables:
		nextround['seeded'].append((tables[i].get_team(1), i))
		nextround['unseeded'].append((tables[i].get_team(2), i))
	nextround['seeded'].append((temptable.get_team(1), 'A'))
	nextround['seeded'].append((temptable.get_team(2), 'B'))
	nextround['seeded'].append((temptable.get_team(3), 'C'))
	nextround['seeded'].append((temptable.get_team(4), 'D'))
	nextround['unseeded'].append((temptable.get_team(5), 'D'))
	nextround['unseeded'].append((temptable.get_team(6), 'E'))
	nextround['unseeded'].append((temptable.get_team(7), 'F'))
	nextround['unseeded'].append((temptable.get_team(8), 'G'))
	redo = 'y'
	while redo == 'y':
		nround = []
		redo = 'n'
		us = copy.deepcopy(nextround['unseeded'])
		for seed in nextround['seeded']:
			t = seed[0]
			temp = []
			for unseed in us:
				if unseed[1] != seed[1] and t.nation != unseed[0].nation:
					temp.append(unseed)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t2 = random.choice(temp)
				nround.append(cp.Match(t2[0], t))
				us.remove(t2)
	return nround

def cup_matchmaker_6(teams):
	matches = []
	n = len(teams)
	nations = {}
	for t in teams:
		try:
			nations[t.nation]+=1
		except:
			nations[t.nation]=1
	rank_n = sorted(nations.items(), key=operator.itemgetter(1))
	mpn = rank_n[-1][1]
	if mpn > int(n/2):
		while len(teams) > 0:
			t1 = random.choice(teams)
			teams.remove(t1)
			t2 = random.choice(teams)
			teams.remove(t2)
			matches.append(cp.Match(t1,t2))
	else:
		redo = 'y'
		while redo == 'y':
			matches = []
			redo = 'n'
			teamscopy = copy.deepcopy(teams)
			while len(teamscopy) > 0:
				t1 = random.choice(teamscopy)
				teamscopy.remove(t1)
				t2 = random.choice(teamscopy)
				teamscopy.remove(t2)
				matches.append(cp.Match(t1,t2))
			for m in matches:
				if m.gethome().nation == m.getaway().nation:
					redo = 'y'
	return matches

def cup_groupmaker(teams):
	pots = {}
	pots['one'] = []
	pots['two'] = []
	pots['three'] = []
	pots['four'] = []
	for i in teams['pot one']:
		pots['one'].append(i)
	t1 = []
	t2 = []
	t3 = []
	t4 = []
	for t in teams['unsorted']:
		if t.league.tier == 'T1':
			t1.append(t)
		elif t.league.tier == 'T2':
			t2.append(t)
		elif t.league.tier == 'T3':
			t3.append(t)
		elif t.league.tier == 'T4':
			t4.append(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['two']) < 8:
			t = random.choice(i)
			pots['two'].append(t)
			i.remove(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['three']) < 8:
			t = random.choice(i)
			pots['three'].append(t)
			i.remove(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['four']) < 8:
			t = random.choice(i)
			pots['four'].append(t)
			i.remove(t)
	redo = 'y'
	while redo == 'y':
		groups = {}
		n = 0
		redo = 'n'
		p2 = copy.deepcopy(pots['two'])
		p3 = copy.deepcopy(pots['three'])
		p4 = copy.deepcopy(pots['four'])
		for seed in pots['one']:
			n+=1
			groups[n] = []
			groups[n].append(seed)
			temp = []
			for team in p2:
				if team.nation != groups[n][0].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p2.remove(t)
			temp = []
			for team in p3:
				if team.nation != groups[n][0].nation and team.nation != groups[n][1].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p3.remove(t)
			temp = []
			for team in p4:
				if team.nation != groups[n][0].nation and team.nation != groups[n][1].nation and team.nation != groups[n][2].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p4.remove(t)
	cupdays = {}
	cuptables = {}
	for i in range(1,13):
		cupdays[i] = CupDay(i)
	for group in groups:
		g = groups[group]
		cuptables[group] = cp.Table(g)
		n = group % 2
		m = cp.Match(g[0], g[2])
		cupdays[1 + n].add_match(group, m)
		m = cp.Match(g[1], g[3])
		cupdays[1 + n].add_match(group, m)
		m = cp.Match(g[1], g[0])
		cupdays[3 + n].add_match(group, m)
		m = cp.Match(g[2], g[3])
		cupdays[3 + n].add_match(group, m)
		m = cp.Match(g[3], g[0])
		cupdays[5 + n].add_match(group, m)
		m = cp.Match(g[1], g[2])
		cupdays[5 + n].add_match(group, m)
		m = cp.Match(g[2], g[0])
		cupdays[7 + n].add_match(group, m)
		m = cp.Match(g[3], g[1])
		cupdays[7 + n].add_match(group, m)
		m = cp.Match(g[0], g[1])
		cupdays[9 + n].add_match(group, m)
		m = cp.Match(g[3], g[2])
		cupdays[9 + n].add_match(group, m)
		m = cp.Match(g[0], g[3])
		cupdays[11 + n].add_match(group, m)
		m = cp.Match(g[2], g[1])
		cupdays[11 + n].add_match(group, m)
	return groups, cupdays, cuptables

def cup_groupmaker_1(teams):
	num = int(len(teams)/4)
	pots = {}
	pots['one'] = []
	pots['two'] = []
	pots['three'] = []
	pots['four'] = []
	t1 = []
	t2 = []
	t3 = []
	t4 = []
	for t in teams:
		if t.league.tier == 'T1':
			t1.append(t)
		elif t.league.tier == 'T2':
			t2.append(t)
		elif t.league.tier == 'T3':
			t3.append(t)
		elif t.league.tier == 'T4':
			t4.append(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['one']) < num:
			t = random.choice(i)
			pots['one'].append(t)
			i.remove(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['two']) < num:
			t = random.choice(i)
			pots['two'].append(t)
			i.remove(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['three']) < num:
			t = random.choice(i)
			pots['three'].append(t)
			i.remove(t)
	for i in [t1,t2,t3,t4]:
		while len(i) > 0 and len(pots['four']) < num:
			t = random.choice(i)
			pots['four'].append(t)
			i.remove(t)
	redo = 'y'
	while redo == 'y':
		groups = {}
		n = 0
		redo = 'n'
		p2 = copy.deepcopy(pots['two'])
		p3 = copy.deepcopy(pots['three'])
		p4 = copy.deepcopy(pots['four'])
		for seed in pots['one']:
			n+=1
			groups[n] = []
			groups[n].append(seed)
			temp = []
			for team in p2:
				if team.nation != groups[n][0].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p2.remove(t)
			temp = []
			for team in p3:
				if team.nation != groups[n][0].nation and team.nation != groups[n][1].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p3.remove(t)
			temp = []
			for team in p4:
				if team.nation != groups[n][0].nation and team.nation != groups[n][1].nation and team.nation != groups[n][2].nation:
					temp.append(team)
			if len(temp) == 0:
				redo = 'y'
				break
			else:
				t = random.choice(temp)
				groups[n].append(t)
				p4.remove(t)
	cupdays = {}
	cuptables = {}
	for i in range(1,7):
		cupdays[i] = CupDay(i)
	for group in groups:
		g = groups[group]
		cuptables[group] = cp.Table(g)
		m = cp.Match(g[0], g[2])
		cupdays[1].add_match(group, m)
		m = cp.Match(g[1], g[3])
		cupdays[1].add_match(group, m)
		m = cp.Match(g[1], g[0])
		cupdays[2].add_match(group, m)
		m = cp.Match(g[2], g[3])
		cupdays[2].add_match(group, m)
		m = cp.Match(g[3], g[0])
		cupdays[3].add_match(group, m)
		m = cp.Match(g[1], g[2])
		cupdays[3].add_match(group, m)
		m = cp.Match(g[2], g[0])
		cupdays[4].add_match(group, m)
		m = cp.Match(g[3], g[1])
		cupdays[4].add_match(group, m)
		m = cp.Match(g[0], g[1])
		cupdays[5].add_match(group, m)
		m = cp.Match(g[3], g[2])
		cupdays[5].add_match(group, m)
		m = cp.Match(g[0], g[3])
		cupdays[6].add_match(group, m)
		m = cp.Match(g[2], g[1])
		cupdays[6].add_match(group, m)
	return groups, cupdays, cuptables
	
def play_final(team1, team2):
	n1 = team1.getname()
	n2 = team2.getname()
	final = g.auto_game(team1, team2)
	s1 = final[0]
	s2 = final[1]
	if final[0] == final[1]:
		final = g.auto_game_extra_time(team1, team2, final[0], final[1])
		s1 = final[0]
		s2 = final[1]
		if final[0] == final[1]:
			pens = g.auto_game_penalties(team1, team2)
			if pens[2] > pens[3]:
				print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2}-{:<2}p'.format('\u0332'.join(n1 + ' '), s1, s2, n2, pens[2], pens[3], field_size=31+len(n1)))
				return team1, team2
			elif pens[3] > pens[2]:
				print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2}-{:<2}p'.format(n1, s1, s2, '\u0332'.join(n2 + ' '), pens[2], pens[3], field_size=31+len(n2)))
				return team2, team1
		elif final[0] > final[1]:
			print('{:>{field_size}s}{:2} {:2}  {:<30s}  aet'.format('\u0332'.join(n1 + ' '), s1, s2, n2, field_size=31+len(n1)))
			return team1, team2
		elif final[1] > final[0]:
			print('{:>30s} {:2} {:2}  {:<{field_size}s} aet'.format(n1, s1, s2, '\u0332'.join(n2 + ' '), field_size=31+len(n2)))
			return team2, team1
	elif final[0] > final[1]:
		print('{:>{field_size}s}{:2} {:2}  {:<30s}  '.format('\u0332'.join(n1 + ' '), s1, s2, n2, field_size=31+len(n1)))
		return team1, team2
	elif final[1] > final[0]:
		print('{:>30s} {:2} {:2}  {:<{field_size}s} '.format(n1, s1, s2, '\u0332'.join(n2 + ' '), field_size=31+len(n2)))
		return team2, team1
	
def play_final_silent(team1, team2):
	n1 = team1.getname()
	n2 = team2.getname()
	final = g.auto_game(team1, team2)
	s1 = final[0]
	s2 = final[1]
	if final[0] == final[1]:
		final = g.auto_game_extra_time(team1, team2, final[0], final[1])
		s1 = final[0]
		s2 = final[1]
		if final[0] == final[1]:
			pens = g.auto_game_penalties(team1, team2)
			if pens[2] > pens[3]:
				return team1, team2
			elif pens[3] > pens[2]:
				return team2, team1
		elif final[0] > final[1]:
			return team1, team2
		elif final[1] > final[0]:
			return team2, team1
	elif final[0] > final[1]:
		return team1, team2
	elif final[1] > final[0]:
		return team2, team1

def first_legs_silent(games):
	results = {}
	n = 0
	for match in games:
		n+=1
		result = g.auto_game(match.gethome(), match.getaway())
		results[n] = {}
		results[n]['first leg'] = [match.gethome().getname(), result[0], result[1], match.getaway().getname()]
		results[n]['second leg'] = cp.Match(match.getaway(), match.gethome())
	return results

def first_legs(games):
	results = {}
	n = 0
	for match in games:
		n+=1
		result = g.auto_game(match.gethome(), match.getaway())
		results[n] = {}
		results[n]['first leg'] = [match.gethome().getname(), result[0], result[1], match.getaway().getname()]
		results[n]['second leg'] = cp.Match(match.getaway(), match.gethome())
	for m in results:
		print('{:>30s} {:2} {:2}  {:<30s}'.format(results[m]['first leg'][0], results[m]['first leg'][1], results[m]['first leg'][2], results[m]['first leg'][3]))
	return results

def second_legs_silent(games, awgr_rt='Yes', awgr_et='Yes'):
	results = {}
	results['winners'] = []
	results['losers'] = []
	for fixture in games:
		match = games[fixture]
		teama = match['second leg'].gethome()
		teamb = match['second leg'].getaway()
		second_leg = g.auto_game(teama, teamb)
		match['second leg'] = [teama.getname(), second_leg[0], second_leg[1], teamb.getname()]
		n1 = teama.getname()
		n2 = teamb.getname()
		flg1 = match['first leg'][2]
		flg2 = match['first leg'][1]
		slg1 = second_leg[0]
		slg2 = second_leg[1]
		if match['first leg'][1] + match['second leg'][2] > match['first leg'][2] + match['second leg'][1]:
			results['winners'].append(teamb)
			results['losers'].append(teama)
		elif match['first leg'][2] + match['second leg'][1] > match['first leg'][1] + match['second leg'][2]:
			results['winners'].append(teama)
			results['losers'].append(teamb)
		elif awgr_rt == 'Yes':
			if flg2 > slg1:
				results['winners'].append(teama)
				results['losers'].append(teamb)
			elif slg2 > flg1:
				results['winners'].append(teamb)
				results['losers'].append(teama)
			else:
				e1, e2 = g.auto_game_extra_time(teama, teamb, match['second leg'][1], match['second leg'][2])
				if e1 > e2:
					results['winners'].append(teama)
					results['losers'].append(teamb)
				elif e2 > e1:
					results['winners'].append(teamb)
					results['losers'].append(teama)
				elif awgr_et == 'Yes':
					if e2 > 0:
						results['winners'].append(teamb)
						results['losers'].append(teama)
					else:	
						penalties = g.auto_game_penalties(teama, teamb)
						results['winners'].append(penalties[0])
						results['losers'].append(penalties[1])
				else:
					penalties = g.auto_game_penalties(teama, teamb)
					results['winners'].append(penalties[0])
					results['losers'].append(penalties[1])
		else:
			e1, e2 = g.auto_game_extra_time(teama, teamb, match['second leg'][1], match['second leg'][2])
			if e1 > e2:
				results['winners'].append(teama)
				results['losers'].append(teamb)
			elif e2 > e1:
				results['winners'].append(teamb)
				results['losers'].append(teama)
			elif awgr_et == 'Yes':
				if e2 > 0:
					results['winners'].append(teamb)
					results['losers'].append(teama)
				else:	
					penalties = g.auto_game_penalties(teama, teamb)
					results['winners'].append(penalties[0])
					results['losers'].append(penalties[1])
			else:
				penalties = g.auto_game_penalties(teama, teamb)
				results['winners'].append(penalties[0])
				results['losers'].append(penalties[1])
	return results

def second_legs(games, awgr_rt='Yes', awgr_et='Yes'):
	results = {}
	results['winners'] = []
	results['losers'] = []
	for fixture in games:
		match = games[fixture]
		teama = match['second leg'].gethome()
		teamb = match['second leg'].getaway()
		second_leg = g.auto_game(teama, teamb)
		match['second leg'] = [teama.getname(), second_leg[0], second_leg[1], teamb.getname()]
		n1 = teama.getname()
		n2 = teamb.getname()
		flg1 = match['first leg'][2]
		flg2 = match['first leg'][1]
		slg1 = second_leg[0]
		slg2 = second_leg[1]
		if match['first leg'][1] + match['second leg'][2] > match['first leg'][2] + match['second leg'][1]:
			results['winners'].append(teamb)
			results['losers'].append(teama)
			print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}'.format(n1, slg1, slg2, '\u0332'.join(n2 + ' '), slg1+flg1, slg2+flg2, field_size=31+len(n2)))
		elif match['first leg'][2] + match['second leg'][1] > match['first leg'][1] + match['second leg'][2]:
			results['winners'].append(teama)
			results['losers'].append(teamb)
			print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2}'.format('\u0332'.join(n1 + ' '), slg1, slg2, n2, slg1+flg1, slg2+flg2, field_size=31+len(n1)))
		elif awgr_rt == 'Yes':
			if flg2 > slg1:
				results['winners'].append(teama)
				results['losers'].append(teamb)
				print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2}  oag'.format('\u0332'.join(n1 + ' '), slg1, slg2, n2, slg1+flg1, slg2+flg2, field_size=31+len(n1)))
			elif slg2 > flg1:
				results['winners'].append(teamb)
				results['losers'].append(teama)
				print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}  oag'.format(n1, slg1, slg2, '\u0332'.join(n2 + ' '), slg1+flg1, slg2+flg2, field_size=31+len(n2)))	
			else:
				e1, e2 = g.auto_game_extra_time(teama, teamb, match['second leg'][1], match['second leg'][2])
				if e1 > e2:
					results['winners'].append(teama)
					results['losers'].append(teamb)
					print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2}  aet'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n1)))
				elif e2 > e1:
					results['winners'].append(teamb)
					results['losers'].append(teama)
					print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}  aet'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n2)))
				elif awgr_et == 'Yes':
					if e2 > 0:
						results['winners'].append(teamb)
						results['losers'].append(teama)
						print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}  oagaet'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n2)))
					else:	
						penalties = g.auto_game_penalties(teama, teamb)
						results['winners'].append(penalties[0])
						results['losers'].append(penalties[1])
						if penalties[2] > penalties[3]:
							print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2} {:2}-{:<2}p'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n1)))
						else:
							print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2} {:2}-{:<2}p'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n2)))
				else:
					penalties = g.auto_game_penalties(teama, teamb)
					results['winners'].append(penalties[0])
					results['losers'].append(penalties[1])
					if penalties[2] > penalties[3]:
						print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2} {:2}-{:<2}p'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n1)))
					else:
						print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2} {:2}-{:<2}p'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n2)))
		else:
			e1, e2 = g.auto_game_extra_time(teama, teamb, match['second leg'][1], match['second leg'][2])
			if e1 > e2:
				results['winners'].append(teama)
				results['losers'].append(teamb)
				print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2}  aet'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n1)))
			elif e2 > e1:
				results['winners'].append(teamb)
				results['losers'].append(teama)
				print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}  aet'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n2)))
			elif awgr_et == 'Yes':
				if e2 > 0:
					results['winners'].append(teamb)
					results['losers'].append(teama)
					print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2}  oageat'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, field_size=31+len(n2)))
				else:	
					penalties = g.auto_game_penalties(teama, teamb)
					results['winners'].append(penalties[0])
					results['losers'].append(penalties[1])
					if penalties[2] > penalties[3]:
						print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2} {:2}-{:2}p'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n1)))
					else:
						print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2} {:2}-{:2}p'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n2)))
			else:
				penalties = g.auto_game_penalties(teama, teamb)
				results['winners'].append(penalties[0])
				results['losers'].append(penalties[1])
				if penalties[2] > penalties[3]:
					print('{:>{field_size}s}{:2} {:2}  {:<30s}  {:2} {:2} {:2}-{:2}p'.format('\u0332'.join(n1 + ' '), slg1+e1, slg2+e2, n2, slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n1)))
				else:
					print('{:>30s} {:2} {:2}  {:<{field_size}s} {:2} {:2} {:2}-{:2}p'.format(n1, slg1+e1, slg2+e2, '\u0332'.join(n2 + ' '), slg1+flg1+e1, slg2+flg2+e2, penalties[2], penalties[3], field_size=31+len(n2)))
	return results


