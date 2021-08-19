import random
import copy
import itertools
import operator
import math
from bisect import bisect as _bisect
from itertools import repeat as _repeat
import tabulate
import numpy as np

#strategies = {'D':{'GK':1.3, 'DF':1.7, 'MD':0.7, 'AT':0.3, 'FI':0.7}, 'C':{'GK':1, 'DF':1.4, 'MD':1, 'AT':0.6, 'FI':1.3}, 'B':{'GK':1, 'DF':1, 'MD':1, 'AT':1, 'FI':1}, 'A':{'GK':0.6, 'DF':0.5, 'MD':1.4, 'AT':1.5, 'FI':1.5}, 'E':{'GK':0.3, 'DF':0.2, 'MD':1.5, 'AT':2, 'FI':1.7}}
strategies = {'F':{'GK':1.05, 'DF':1.05, 'MD':1, 'AT':0.8, 'FI':0.5}, 'D':{'GK':1.2, 'DF':1.2, 'MD':0.9, 'AT':0.8, 'FI':1.1}, 'C':{'GK':1.1, 'DF':1.1, 'MD':0.9, 'AT':0.9, 'FI':1}, 'B':{'GK':1, 'DF':1, 'MD':1, 'AT':1, 'FI':1}, 'A':{'GK':0.9, 'DF':0.9, 'MD':1.1, 'AT':1.1, 'FI':1.1}, 'E':{'GK':0.9, 'DF':0.9, 'MD':1.2, 'AT':1.2, 'FI':1.2}}

def sp(num):
    if num == 1:
        return 0
    else:
        return 1

chance = ["chance", "chances"]
goal = ["goal", "goals"]

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

#def attack(team, strategy, n):
#	return (team.stats['AT']*strategy['AT']+team.stats['MD']*strategy['MD']+team.stats['TP']+team.stats['MO']+(team.stats['FI'])*random.randint(1,n))

#def defend(team, strategy, n):
#	return (team.stats['GK']*strategy['GK']+team.stats['DF']*strategy['DF']+team.stats['MD']*strategy['MD']+team.stats['TP']+team.stats['MO']+(team.stats['FI'])*random.randint(1,n))

#def attack(team, strategy, home='No'):
#	n = 4
#	at = team.stats['AT']*strategy['AT']*random.randint(1,5)
#	if at >= 0.8:
#		n+=1
#	md = team.stats['MD']*strategy['MD']*random.randint(1,5)
#	if md >= 0.8:
#		n+=1
#	tp = team.stats['TP']*random.randint(1,5)
#	if tp >= 0.8:
#		n+=1
#	mo = team.stats['MO']*random.randint(1,5)
#	if mo >= 0.8:
#		n+=1
#	fi = team.stats['FI']*random.randint(1,5)
#	if mo >= 0.8:
#		n+=1
#	if team in home:
#		n+=1
#	return random.randint(1,n)
#
#def defend(team, strategy, home='No'):
#	n = 4
#	gk = team.stats['GK']*strategy['GK']*random.randint(1,6)
#	if gk >= 0.8:
#		n+=1
#	df = team.stats['DF']*strategy['DF']*random.randint(1,6)
#	if df >= 0.8:
#		n+=1
#	md = team.stats['MD']*strategy['MD']*random.randint(1,6)
#	if md >= 0.8:
#		n+=1
#	tp = team.stats['TP']*random.randint(1,6)
#	if tp >= 0.8:
#		n+=1
#	mo = team.stats['MO']*random.randint(1,6)
#	if mo >= 0.8:
#		n+=1
#	fi = team.stats['FI']*random.randint(1,6)
#	if mo >= 0.8:
#		n+=1
#	if team in home:
#		n+=1
#	return random.randint(1,n)


def attack(team, strategy, home='No'):
	n = 4
	at = team.stats['AT']*strategy['AT']
	if at >= 0.8:
		n+=1
	md = team.stats['MD']*strategy['MD']
	if md >= 0.8:
		n+=1
	tp = team.stats['TP']
	if tp >= 0.8:
		n+=1
	mo = team.stats['MO']
	if mo >= 0.8:
		n+=1
	fi = team.stats['FI']
	if fi >= 0.8:
		n+=1
	if team in home:
		n+=1
	return random.randint(1,n)

def defend(team, strategy, home='No'):
	n = 4
	gk = team.stats['GK']*strategy['GK']
	if gk >= 0.8:
		n+=1
	df = team.stats['DF']*strategy['DF']
	if df >= 0.8:
		n+=1
	md = team.stats['MD']*strategy['MD']
	if md >= 0.8:
		n+=1
	tp = team.stats['TP']
	if tp >= 0.8:
		n+=1
	mo = team.stats['MO']
	if mo >= 0.8:
		n+=1
	fi = team.stats['FI']
	if fi >= 0.8:
		n+=1
	if team in home:
		n+=1
	return random.randint(1,n)

def phase(team1, team2, strategy1, strategy2, home='None'):
	nc = 0
	if team1 in home:
		at = team1.stats['AT']*strategy1['AT']*random.randint(1,7)
	else:
		at = team1.stats['AT']*strategy1['AT']*random.randint(1,6)
	if at >= 0.8:
		nc+=1
	if team2 in home:
		df = team2.stats['DF']*strategy2['DF']*random.randint(1,7)
	else:
		df = team2.stats['DF']*strategy2['DF']*random.randint(1,6)
	if df >= 0.8:
		nc-=1
	if nc < 0:
		chances = int(choices([0,1,2], weights=[85,13,2])[0])
	elif nc == 0:
		chances = int(choices([0,1,2], weights=[70,25,5])[0])
	elif nc > 0:
		chances = int(choices([0,1,2], weights=[35,50,15])[0])
	return chances

def game(team1, team2, options='None'):
	hts = team1.stats
	ats = team2.stats
	team1goals = 0
	team2goals = 0
	if 'Neutral' in options:
		hometeam = []
	else:
		hometeam = [team1]
	for turn in range(10):
		c = phase(team1, team2, strategies[hts['SS']], strategies[ats['SS']], home=hometeam)
		for g in range(c):
			if attack(team1, strategies[hts['SS']], home=hometeam)-defend(team2, strategies[ats['SS']], home=hometeam) > 0:
				team1goals+=1
				team1.changestat('MO', hts['MO']+float(choices([0.03,0.05,0.07], weights=[30,50,20])[0]))
				team2.changestat('MO', ats['MO']-float(choices([0.03,0.05,0.07,-0.03], weights=[30,45,20,5])[0]))
		c = phase(team2, team1, strategies[ats['SS']], strategies[hts['SS']], home=hometeam)
		for g in range(c):
			if attack(team2, strategies[ats['SS']], home=hometeam)-defend(team1, strategies[hts['SS']], home=hometeam) > 0:
				team2goals+=1
				team2.changestat('MO', ats['MO']+float(choices([0.03,0.05,0.07], weights=[30,50,20])[0]))
				team1.changestat('MO', hts['MO']-float(choices([0.03,0.05,0.07,-0.03], weights=[30,45,20,5])[0]))
		team1.changestat('FI', hts['FI']-float(choices([0.02,0.03,0.05], weights=[30,50,20])[0])*strategies[hts['SS']]['FI'])
		team2.changestat('FI', ats['FI']-float(choices([0.02,0.03,0.05], weights=[30,50,20])[0])*strategies[ats['SS']]['FI'])
		if hts['FI'] <= 0:
			team1.changestat('FI', 0.01)
		if ats['FI'] <= 0:
			team2.changestat('FI', 0.01)
		team1.changestat('SS', strategy_changer(team1goals, team2goals, hts, turn))
		team2.changestat('SS', strategy_changer(team2goals, team1goals, ats, turn))
	#	print turn, team1.getname(), hts['MO'], hts['FI'], hts['SS'], int(team1goals), team2.getname(), ats['MO'], ats['FI'], ats['SS'], int(team2goals)
	return team1.getname(), int(team1goals), int(team2goals), team2.getname()

def game_interactive(team_p, team_c, options='None'):
	tps = team_p.stats
	tcs = team_c.stats
	team_p_goals = 0
	team_c_goals = 0
	if 'Neutral' in options:
		hometeam = []
	elif 'Team_p_home':
		hometeam = [team_p]
	elif 'Team_c_home':
		hometeam = [team_c]
	for turn in range(10):
		print "It's turn " + str(turn+1)
		strat = raw_input("Choose a strategy (F: Fitness-first; D: Defensive; C: Cautious, B: Balanced, A: Attacking, E:Extreme)")
		while strat not in ['A', 'B', 'C', 'D', 'E', 'F']:
			strat = raw_input("Please only input A, B, C, D, E, or F. (F: Fitness-first; D: Defensive; C: Cautious, B: Balanced, A: Attacking, E:Extreme)")
		c = phase(team_p, team_c, strategies[strat], strategies[tcs['SS']], home=hometeam)
		g=0
		for y in range(c):
			if attack(team_p, strategies[strat], home=hometeam)-defend(team_c, strategies[tcs['SS']], home=hometeam) > 0:
				g+=1
				team_p_goals+=1
				team_p.changestat('MO', tps['MO']+float(choices([0.03,0.05,0.07], weights=[30,50,20])[0]))
				team_c.changestat('MO', tcs['MO']-float(choices([0.03,0.05,0.07,-0.03], weights=[30,45,20,5])[0]))
		print "You have created " + str(c) + " " + str(chance[sp(c)]) + " and have scored " + str(g) + " " + str(goal[sp(g)]) + "."
		c = phase(team_c, team_p, strategies[tcs['SS']], strategies[strat], home=hometeam)
		g=0
		for y in range(c):
			if attack(team_c, strategies[tcs['SS']], home=hometeam)-defend(team_p, strategies[tps['SS']], home=hometeam) > 0:
				g+=1
				team_c_goals+=1
				team_c.changestat('MO', tcs['MO']+float(choices([0.03,0.05,0.07], weights=[30,50,20])[0]))
				team_p.changestat('MO', tps['MO']-float(choices([0.03,0.05,0.07,-0.03], weights=[30,45,20,5])[0]))
		team_p.changestat('FI', tps['FI']-float(choices([0.02,0.03,0.05], weights=[30,50,20])[0])*strategies[strat]['FI'])
		team_c.changestat('FI', tcs['FI']-float(choices([0.02,0.03,0.05], weights=[30,50,20])[0])*strategies[tcs['SS']]['FI'])
		if tps['FI'] <= 0:
			team_p.changestat('FI', 0.01)
		if tcs['FI'] <= 0:
			team_c.changestat('FI', 0.01)
		team_c.changestat('SS', strategy_changer(team_c_goals, team_p_goals, tcs, turn))
		print "The opposing team created " + str(c) + " " + str(chance[sp(c)]) + " and scored " + str(g) + " " + str(goal[sp(g)]) + "."
		print "The current score is " + str(team_p_goals) + " to " + str(team_c_goals) + "."
	
def strategy_changer(goals1, goals2, teamstats, turn, options='None'):
	strat = teamstats['SS']
	fit = teamstats['FI']
	men = teamstats['ME']
	tac = teamstats['TP']
	newstrat = teamstats['SS']
	if men == 1:
		if goals1<goals2-1:
			if turn < 4:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[80,10,5,3,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,40,20,5,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[85,7,4,2,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,25,5,4,3,3])[0])
			elif turn > 8:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[90,3,3,2,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[70,10,8,5,4,3])[0])
		if goals1<goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,30,20,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,50,30,5,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,25,10,3,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,40,15,6,5,4])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,20,10,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,30,20,4,4,2])[0])
		if goals1==goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,30,40,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,40,20,15,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,35,25,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,45,20,6,3,1])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[80,10,5,3,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[70,15,8,4,2,1])[0])
		if goals1>goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,40,20,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,50,25,10,7,3])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,45,13,4,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,55,15,12,5,3])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,50,20,7,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[6,80,7,3,3,1])[0])
		if goals1>goals2+1:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,60,15,3,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,55,25,5,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,35,10,8,5,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,65,20,5,3,2])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,40,30,10,6,4])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,85,6,4,1,1])[0])
	elif men == 2:
		if goals1<goals2-1:
			if turn < 4:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,20,10,10,10,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,15,20,15,20,20])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,5,15,20,10,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,5,15,20,30,25])[0])
			elif turn > 8:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,5,10,10,25,30])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,5,5,9,20,60])[0])
		if goals1<goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[25,5,5,15,30,20])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,3,5,20,45,25])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,10,15,15,20,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,5,5,14,45,30])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,1,4,15,25,45])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,2,3,4,25,65])[0])
		if goals1==goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,4,6,30,20,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,2,2,40,35,20])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,5,10,30,15,5])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,1,4,50,30,10])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[80,10,5,3,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[70,15,8,4,2,1])[0])
		if goals1>goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,10,20,25,6,4])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,15,25,15,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[45,5,30,17,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,10,45,20,3,2])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,55,25,2,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,75,20,1,1,1])[0])
		if goals1>goals2+1:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,20,25,10,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,25,30,8,4,3])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,15,25,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,15,35,12,2,1])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,5,25,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,30,40,7,2,1])[0])
	elif men == 3:
		if goals1<goals2-1:
			if turn < 4:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,5,10,15,10,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,10,15,25,15,15])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,10,20,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,15,25,10,12,8])[0])
			elif turn > 8:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[80,2,5,7,3,3])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,5,10,5,15,5])[0])
		if goals1<goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,5,20,20,15,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,10,15,30,30,10])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,7,13,20,15,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,15,20,30,15,10])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,10,12,18,5,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,10,10,20,30,25])[0])
		if goals1==goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,5,10,50,12,8])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,6,9,60,15,5])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,10,10,30,20,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,7,10,40,25,15])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,5,20,25,5,5])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,10,25,25,12,8])[0])
		if goals1>goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,20,30,8,7,5])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,25,35,25,3,2])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,25,35,6,3,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,30,40,20,3,2])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,25,30,8,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,30,40,17,6,4])[0])
		if goals1>goals2+1:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,5,10,43,5,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,5,10,60,10,5])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,10,15,20,4,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,10,12,65,6,4])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,5,15,15,4,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,30,43,20,3,2])[0])
	elif men == 4:
		if goals1<goals2-1:
			if turn < 4:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,5,10,10,30,25])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,6,14,5,40,30])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[25,3,7,15,30,20])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,5,5,7,45,35])[0])
			elif turn > 8:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,1,2,10,30,37])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,2,6,30,60])[0])
		if goals1<goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,3,7,20,30,25])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,2,4,11,50,30])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,3,7,15,28,27])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,1,2,12,45,35])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[22,2,2,14,25,35])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,2,3,4,20,70])[0])
		if goals1==goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,2,3,10,60,15])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,3,5,70,20])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[12,1,2,5,50,30])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,5,52,40])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[13,2,2,8,30,45])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,2,25,70])[0])
		if goals1>goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[25,10,15,25,15,10])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[6,14,25,45,7,3])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,20,30,10,8,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[7,23,45,25,4,1])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,25,30,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,38,40,17,2,1])[0])
		if goals1>goals2+1:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,20,30,5,3,2])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,25,40,2,2,1])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[45,25,25,2,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[20,25,40,10,3,2])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[60,12,17,7,3,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[45,15,25,12,2,1])[0])
	elif men == 5:
		if goals1<goals2-1:
			if turn < 4:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,2,3,10,30,40])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,3,4,6,40,45])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[17,1,2,10,25,45])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,1,2,5,40,50])[0])
			elif turn > 8:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[18,1,1,5,30,45])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,2,25,70])[0])
		if goals1<goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,1,2,7,50,30])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,2,6,55,35])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,2,3,5,40,40])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,2,55,40])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[12,1,2,15,30,40])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,2,15,80])[0])
		if goals1==goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[15,3,7,20,30,25])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[6,4,6,14,40,30])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[12,1,2,5,50,30])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,5,52,40])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[10,1,2,7,60,20])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[1,1,1,1,46,50])[0])
		if goals1>goals2:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,5,10,40,10,5])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[5,6,9,50,20,10])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,10,12,28,8,7])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[3,12,25,30,20,10])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[40,20,30,2,7,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[2,38,40,17,2,1])[0])
		if goals1>goals2+1:
			if turn < 4:
				if fit < 0.8:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,15,25,7,2,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[35,20,30,8,4,3])[0])
			elif turn >= 4 and turn <= 8:
				if fit < 0.6:
					ns = str(choices(['F','D','C','B','A','E'], weights=[48,12,14,24,1,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[30,20,25,20,3,2])[0])
			elif turn > 8:
				if fit < 0.7:
					ns = str(choices(['F','D','C','B','A','E'], weights=[55,15,20,6,3,1])[0])
				else:
					ns = str(choices(['F','D','C','B','A','E'], weights=[50,20,26,2,1,1])[0])
	return ns
		
def mentality_calculator(team1, team2, table, day, options='None'):
	pos1 = table.get_position(team1)
	pos2 = table.get_position(team2)
	men = 3
	if pos1 - pos2 > 8:
		men = 5
	elif pos1 - pos2 < -8:
		men = 1
	if day < 5:
		men = 3
	if abs(pos1 - pos2) < 5 and (team1.getstats()['FI'] > 0.8 or team1.getstats()['MO'] > 0.8):
		men = 4
	elif abs(pos1 - pos2) < 5 and (team1.getstats()['FI'] < 0.8 and team1.getstats()['MO'] < 0.8):
		men = 2
	return men

#for t in [3,4,5]:
#        for g in [3,4,5]:
#                print t,g
#                check = []
#                for i in range(100000):
#                        check.append(f.attack(l[t], strategies['B'])-f.defend(l[g], strategies['B']))
#                for i in plt.hist(check, bins=bins)[0]:
#                        print i


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
		self.teams_list = []
		for sq in teams:
			self.teams[sq.getname()] = [0,0,0,0,0,0,0,0," "]
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
		self.teams[team.getname()] = [curr_points+points,curr_gamesplayed+gamesplayed,curr_gameswon+gameswon,curr_gameslost+gameslost,curr_gamesdrawn+gamesdrawn,curr_goalfor+goalsfor,curr_goalagainst+goalsagainst,curr_goaldiff+(goalsfor-goalsagainst), curr_form]

	def get_position(self, team):
		sort_tab = sorted(sorted(sorted(sorted([[k] + v for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True)
		positions = []
		for i in sort_tab:
			positions.append(i[0])
		return positions.index(team.getname()) + 1

	def display_table(self):
		headers = ["Position", "Team", "Points", "GP", "W", "L", "D", "GF", "GA", "Diff", "Recent Form"]
		print(tabulate.tabulate(sorted(sorted(sorted(sorted([[k] + v for k,v, in self.teams.items()], key=operator.itemgetter(0)), key=operator.itemgetter(6), reverse=True), key=operator.itemgetter(8), reverse=True), key=operator.itemgetter(1), reverse=True), headers = headers, showindex=range(1,21)))

class Team_older(object):
	def __init__(self, name, strength):
		self.name = name
		self.strength = float(strength)

	def getname(self):
		return self.name

	def getstrength(self):
		return self.strength

class Team_old(object):	
	def __init__(self, name, stats):
		self.name = name
		self.stats = {}
		self.stats['GK'] = float(stats[0])
		self.stats['DF'] = float(stats[1])
		self.stats['MD'] = float(stats[2])
		self.stats['AT'] = float(stats[3])
		self.stats['FI'] = float(stats[4])
		self.stats['MO'] = float(stats[5])
		self.stats['TP'] = float(stats[6])

class Team(object):
	def __init__(self, name, stats):
		self.name = name
		self.stats = {}
		self.stats['GK'] = float(stats[0])
		self.stats['DF'] = float(stats[1])
		self.stats['MD'] = float(stats[2])
		self.stats['AT'] = float(stats[3])
		self.stats['TP'] = float(stats[4])
		self.stats['FI'] = float(1)
		self.stats['MO'] = float(1)
		self.stats['ME'] = float(3)
		self.stats['SS'] = 'B'

	def changestat(self, stat, value):
		self.stats[stat] = value

	def getname(self):
		return self.name

	def getstat(self, stat):
		return self.stats[stat]

	def getstats(self):
		return self.stats

	def set_calendar(self, calendar):
		self.calendar = calendar

	def getposition(self, table):
		return table.get_position(self)

	def getcalendar(self):
		for i in self.calendar:
			print self.calendar[i]

class Match(object):
	def __init__(self, hometeam, awayteam):
		self.hometeam = hometeam
		self.awayteam = awayteam

	def gethome(self):
		return self.hometeam
	
	def getaway(self):
		return self.awayteam

	def getread(self):
		return '{:>20s}   -    {:<20s}'.format(self.gethome().getname(), self.getaway().getname())
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

def makeleague_old(inputfile):
	dataset = []
	f = open(inputfile)
	opened = f.readlines()
	for line in opened:
		name,strength = line.split(",")
		dataset.append(Team_old(name.strip(),strength.strip()))
	f.close()
	return dataset

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

def createleague(inputfile, options='None'):
	dataset = []
	f = open(inputfile)
	opened = f.readlines()
	league = []
	teams = []
	for line in opened:
		name = line.strip()
		teams.append(name)
	f.close()
	teams2 = random.sample(teams, 20)
	for t in teams2:
		ov = choices([3,4,5,6,7,8,9], weights=[2,2,4,4,3,3,2])[0]
		vals = []
		for z in range(0,5):
			vals.append((ov*10-random.randrange(-6,6))/float(100))
		league.append(Team(t,vals))
	return league

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

def playgame_simple(hometeam, awayteam):
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

def playgame(team1, team2, options='None'):
	hts = team1.stats
	ats = team2.stats
	team1goals = 0
	team2goals = 0
	if 'Neutral' in options:
		hometeam = []
	else:
		hometeam = [team1]
	for turns in range(9):
		c = phase(team1, team2, strategies['B'], strategies['B'], home=hometeam)
		for g in range(c):
			if attack(team1, strategies['B'], home=hometeam)-defend(team2, strategies['B'], home=hometeam) > 0:
				team1goals+=1
		c = phase(team2, team1, strategies['B'], strategies['B'], home=hometeam)
		for g in range(c):
			if attack(team2, strategies['B'], home=hometeam)-defend(team1, strategies['B'], home=hometeam) > 0:
				team2goals+=1
	return team1.getname(), int(team1goals), int(team2goals), team2.getname()

def gameday(day, table):
	for match in day.matches:
		t1 = match.gethome()
		t2 = match.getaway()
		t1.changestat('ME', mentality_calculator(t1, t2, table, day))
		t2.changestat('ME', mentality_calculator(t2, t1, table, day))
		result = game(match.gethome(), match.getaway())
		team1 = result[0]
		ght = result[1]
		gat = result[2]
		team2 = result[3]
		print '{:>20s} {:2} {:2}  {:<20s}'.format(team1, ght, gat, team2)
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
	fitness = open('fitness.out', 'w')
	for day in year.days:
		gameday(year.days[day], table)
		for team in table.teams_list:
			postmatch(team)
			fitness.write(str(team.getname()) + "," + str(team.getstat('ME')) + "\n")
		raw_input("Press Enter to continue:")
