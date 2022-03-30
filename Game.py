import numpy as np
import math
import random
import operator
from bisect import bisect as _bisect
from itertools import repeat as _repeat
from collections import Counter

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

def normrand(n):
        num = np.random.normal(n,n/5.)
        if num < 0.01:
                num = 0.01
        elif num >= 2*n-0.01:
                num = 2*n-0.01
        return round(num, 3)

def goleval(f, s):
	n1 = f
	n2 = s
	p1 = math.exp(n1) / (math.exp(n1) + math.exp(n2))
	p2 = math.exp(n2) / (math.exp(n1) + math.exp(n2))
	ev = random.random()
	if ev < p1:
		return 'f'
	else:
		return 's'	

def auto_game(team1, team2, options=None):
	team1w = team1.getaverage()
	team2w = team2.getaverage()
	if team1w - team2w < 0.3:
		draw = 0.5
	else:
		draw = 0.25
	n1 = team1w*4
	n2 = team2w*4
	n3 = draw*6
	p1 = math.exp(n1) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	p2 = math.exp(n2) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	p3 = math.exp(n3) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	ev = random.random()
	if ev < p1:
		g1 = 1
		if team1w > 0.85:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[22,33,20,13,6.4,3,0.5,0.1])[0]
		elif team1w > 0.5:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[39,50,15,3,2.5,0.5,0,0])[0]
		else:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[45,42,10,3,0,0,0,0])[0]
		if team2w > 0.85:
			g2 = choices([1,2,3,4,5,6,7], weights=[40,25,20,6,4,3,2])[0]
		elif team2w > 0.5:
			g2 = choices([1,2,3,4,5,6,7], weights=[15,35,24,8,6,5,4,3])[0]
		else:
			g2 = choices([1,2,3,4,5,6,7], weights=[10,20,30,15,10,8,7])[0]
		g2 = g1 - g2
		if g2 < 0:
			g2 = 0
		return (g1, g2)
	elif ev < p1+p2:
		g1 = 1
		if team2w > 0.85:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[22,33,20,13,6.4,3,0.5,0.1])[0]
		elif team2w > 0.5:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[39,50,15,3,2.5,0.5,0,0])[0]
		else:
			g1 += choices([0,1,2,3,4,5,6,7], weights=[45,42,10,3,0,0,0,0])[0]
		if team1w > 0.85:
			g2 = choices([1,2,3,4,5,6,7], weights=[40,25,20,6,4,3,2])[0]
		elif team1w > 0.5:
			g2 = choices([1,2,3,4,5,6,7], weights=[15,35,24,8,6,5,4,3])[0]
		else:
			g2 = choices([1,2,3,4,5,6,7], weights=[10,20,30,15,10,8,7])[0]
		g2 = g1 - g2
		if g2 < 0:
			g2 = 0
		return (g2, g1)
	else:
		if team1w > 0.85:
			g1 = choices([0,1,2,3,4,5,6,7], weights=[30,25,24,9.5,6.3,5,0.1,0.1])[0]
		elif team1w > 0.5:
			g1 = choices([0,1,2,3,4,5,6,7], weights=[40,34,19,4,2,1,0,0])[0]
		else:
			g1 = choices([0,1,2,3,4,5,6,7], weights=[40,35,20,5,0,0,0,0])[0]
		return (g1, g1)

def auto_game_extra_time(team1, team2, g1, g2):
	team1w = team1.getaverage()
	team2w = team2.getaverage()
	if team1w - team2w < 0.3:
		draw = 0.5
	else:
		draw = 0.25
	n1 = team1w*1.5
	n2 = team2w*1.5
	n3 = draw*4
	p1 = math.exp(n1) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	p2 = math.exp(n2) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	p3 = math.exp(n3) / (math.exp(n1) + math.exp(n3) + math.exp(n2))
	ev = random.random()
	if ev < p1:
		if team1w - team2w > 0.5:
			g1 += choices([1,2,3], weights=[70,20,10])[0]
		elif team1w - team2w > 0.25:
			g1 += choices([1,2,3], weights=[90,7,3])[0]
		else:
			g1 += choices([1,2,3], weights=[97,3,0])[0]
		return (g1, g2)
	elif ev < p1+p2:
		if team2w - team1w > 0.5:
			g2 += choices([1,2,3], weights=[70,20,10])[0]
		elif team2w - team1w > 0.25:
			g2 += choices([1,2,3], weights=[90,7,3])[0]
		else:
			g2 += choices([1,2,3], weights=[97,3,0])[0]
		return (g1, g2)
	else:
		g1 += choices([0,1,2], weights=[90,9.9,0.1])[0]
		g2 = g1 
		return(g1, g2)

def auto_game_penalties(team1, team2):
		t1a = team1.getstat('AT')
		t1g = team1.getstat('GK')
		t2a = team2.getstat('AT')
		t2g = team2.getstat('GK')
		pens1 = {}	
		pens2 = {}
		pens1['tot'] = 0
		pens2['tot'] = 0
		pens1['seq'] = ''
		pens2['seq'] = ''
		for i in range(5):
			if pens2['tot'] - pens1['tot'] > 5 - i:
				break
			if goleval(t1a, t2g*.05) == 'f':
				pens1['tot']+=1
				pens1['seq'] = pens1['seq'] + 'O'
			else:
				pens1['seq'] = pens1['seq'] + 'X'
			if pens2['tot'] - pens1['tot'] > 5 - i - 1:
				break
			if pens1['tot'] - pens2['tot'] > 5 - i:
				break
			if goleval(t2a, t1g*.05) == 'f':
				pens2['tot']+=1
				pens2['seq'] = pens2['seq'] + 'O'
			else:
				pens2['seq'] = pens2['seq'] + 'X'
			if pens1['tot'] - pens2['tot'] > 5 - i - 1:
				break
		if pens1['tot'] > pens2['tot']:
			return (team1, team2, pens1['tot'], pens2['tot'], pens1['seq'], pens2['seq'])	
		elif pens2['tot'] > pens1['tot']:
			return (team2, team1, pens1['tot'], pens2['tot'], pens1['seq'], pens2['seq'])
		else:
			while pens1['tot'] == pens2['tot']:
				if goleval(t1a, t2g*.05) == 'f':
					pens1['tot']+=1
					pens1['seq'] = pens1['seq'] + 'O'
				else:
					pens1['seq'] = pens1['seq'] + 'X'
				if goleval(t2a, t1g*.05) == 'f':
					pens2['tot']+=1
					pens2['seq'] = pens2['seq'] + 'O'
				else:
					pens2['seq'] = pens2['seq'] + 'X'
			if pens1['tot'] > pens2['tot']:
				return (team1, team2, pens1['tot'], pens2['tot'], pens1['seq'], pens2['seq'])	
			elif pens2['tot'] > pens1['tot']:
				return (team2, team1, pens1['tot'], pens2['tot'], pens1['seq'], pens2['seq'])

base_distribution = {
	'E' : {'E': {0:15, 1:55, 2:30}, 'A': {0:20, 1:60, 2:20}, 'B': {0:25, 1:60, 2:15}, 'C': {0:40, 1:50, 2:10}, 'D': {0:55, 1:40, 2:5}, 'F': {0:30, 1:60, 2:10}, 'eff':2},
	'A' : {'E': {0:25, 1:55, 2:20}, 'A': {0:25, 1:65, 2:10}, 'B': {0:30, 1:65, 2:5}, 'C': {0:50, 1:48, 2:2}, 'D': {0:60, 1:39, 2:1}, 'F': {0:35, 1:58, 2:7}, 'eff':1.5},
	'B' : {'E': {0:30, 1:60, 2:10}, 'A': {0:30, 1:65, 2:5}, 'B': {0:50, 1:40, 2:10}, 'C': {0:60, 1:39, 2:1}, 'D': {0:80, 1:20, 2:0}, 'F': {0:55, 1:43, 2:2}, 'eff':1},
	'C' : {'E': {0:50, 1:43, 2:7}, 'A': {0:65, 1:30, 2:5}, 'B': {0:70, 1:29, 2:1}, 'C': {0:80, 1:20, 2:0}, 'D': {0:90, 1:10, 2:0}, 'F': {0:60, 1:39, 2:1}, 'eff': 1.2},
	'D' : {'E': {0:75, 1:24, 2:1}, 'A': {0:80, 1:20, 2:0}, 'B': {0:90, 1:10, 2:0}, 'C': {0:95, 1:5, 2:0}, 'D': {0:97, 1:3, 2:0}, 'F': {0:75, 1:25, 2:0}, 'eff': 1.5},
	'F' : {'E': {0:40, 1:55, 2:5}, 'A': {0:50, 1:40, 2:10}, 'B': {0:55, 1:40, 2:5}, 'C': {0:70, 1:30, 2:0}, 'D': {0:80, 1:20, 2:0}, 'F': {0:65, 1:33, 2:2}, 'eff': 0.5}
	}

personality = {
	'Pragmatic': {'st_parity': [0,30,70,0,0,0], 'st_win': [0,20,30,40,10,0], 'st_lose': [10,50,40,0,0,0], 'fitness': {'fi': 0.4, 'turn': 8, 'score':0}},
	'Aggressive': {'st_parity': [10,30,60,0,0,0], 'st_win': [0,30,50,20,10,0], 'st_lose': [20,70,10,0,0,0], 'fitness': {'fi': 0.3, 'turn': 9, 'score':1}},
	'Cautious': {'st_parity': [0,10,40,50,0,0], 'st_win': [0,0,30,40,30,0], 'st_lose': [0,30,40,20,10,0], 'fitness': {'fi': 0.5, 'turn': 7, 'score':0}},
	'Unambitious': {'st_parity': [0,0,20,50,30,0], 'st_win': [0,0,0,40,60,0], 'st_lose': [40,40,20,0,0,0], 'fitness': {'fi': 0.4, 'turn': 8, 'score':0}}
	}

def stratchanger(g1, g2, turn, fit, pers):
	f = 0
	score = g1 - g2
	if fit < personality[pers]['fitness']['fi']:
		f+=1
	if turn >= personality[pers]['fitness']['turn']:
		f+=1
	if score >= personality[pers]['fitness']['score']:
		f+=1
	if f >= 2:
		return 'F'
	else:
		if score == 0:
			return choices(['E', 'A', 'B', 'C', 'D', 'F'], weights=personality[pers]['st_parity'])[0]
		elif score > 0:
			return choices(['E', 'A', 'B', 'C', 'D', 'F'], weights=personality[pers]['st_win'])[0]
		elif score < 0:
			return choices(['E', 'A', 'B', 'C', 'D', 'F'], weights=personality[pers]['st_lose'])[0]

def effdiff(eff1, eff2):
        somma = int((eff1+eff2)*100)
        res = random.randint(0, somma)
        if res < eff1*100:
                return 'A'
        else:
                return 'B'

def moralechanger(c1, c2, g1, g2, st, mo):
	if st == 'E':
		if g1 < 1:
			mo -= 0.05
		elif c1 < 1:
			mo -= 0.1
		if g1 > 1:
			mo += 0.25
		elif g1 > 0:
			mo += 0.1
		elif c1 > 0:
			mo += 0.03
	elif st == 'A':
		if g1 < 1:
			mo -= 0.03
		elif c1 < 1:
			mo -= 0.05
		if g2 > 1:
			mo -= 0.15
		elif g2 > 0:
			mo -= 0.07
		if g1 > 1:
			mo += 0.21
		elif g1 > 0:
			mo += 0.1
	elif st == 'B' or 'F':
		if g1 > 0:
			mo += 0.1*g1
		if g2 > 0:
			mo -= 0.11*g2
	elif st == 'C':
		if g2 > 1:
			mo -= 0.30
		elif g2 > 0:
			mo -= 0.12
		elif c2 > 0:
			mo -= 0.05
		else:
			mo += 0.03
		if g1 > 0:
			mo += 0.1*2
	elif st == 'D':
		if g2 > 1:
			mo -= 0.35
		elif g2 > 0:
			mo -= 0.15
		elif c2 > 0:
			mo -= 0.08
		else:
			mo += 0.1
		if g1 > 0:
			mo += 0.1*2
	mor = fixval(mo)
	return(mor)

def fixval(val):
	if val < 0:
		val = 0.01
	return round(val, 3)

def game_noninteractive(team1, team2):
	chances1 = 0
	chances2 = 0
	goals1 = 0
	goals2 = 0
	for turn in range(10):
		st1 = stratchanger(goals1, goals2, turn, team1['FI'], team1['PE'])
		st2 = stratchanger(goals2, goals1, turn, team2['FI'], team2['PE'])
		team1['FI'] -= normrand(0.06)*base_distribution[st1]['eff']
		team1['FI'] = fixval(team1['FI'])
		team2['FI'] -= normrand(0.06)*base_distribution[st2]['eff']
		team2['FI'] = fixval(team2['FI'])
		att1 = round(np.average([team1['AT']*2,team1['MD'],team1['MO'],team1['TP'],team1['FI']]), 3)
		def2 = round(np.average([team2['DF']*2,team2['MD'],team2['MO'],team2['TP'],team2['FI']]), 3)
		at = []
		base = base_distribution[st1][st2].copy()
		for i in range(4):
			at.append(effdiff(att1, def2))
		if at.count('A') == 4:
			base[0]-=5
			base[1]+=10
			base[2]+=10
		elif at.count('A') == 3:
			base[1]+=10
			base[2]+=5
		elif at.count('A') == 2:
			base[0]+=5
			base[1]+=5
		elif at.count('A') == 1:
			base[0]+=10
		elif at.count('A') == 0:
			base[0]+=15
			base[1]-=5
			base[2]-=10
		if team1['FI'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team1['FI'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team2['FI'] < 0.1:
			base[0]-=10
		elif team2['FI'] < 0.3:
			base[0]-=5
		if team1['MO'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team1['MO'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team2['MO'] < 0.1:
			base[0]-=10
		elif team2['MO'] < 0.3:
			base[0]-=5
		c1=choices([0,1,2], weights=base.values())[0]
		chances1+=c1
		g1 = 0
		for i in range(c1):
			go1 = round(np.average([team1['AT'],team1['MO'],team1['TP'],team1['FI']]), 3)
			go2 = round(np.average([team2['GK'],team2['MO'],team2['TP'],team2['FI']]), 3)
			if goleval(go1*.1, go2*.8) == 'f':
				g1+=1
				goals1+=1
		att2 = np.average([team2['AT']*2,team2['MD'],team2['MO'],team2['TP'],team2['FI']])
		def1 = np.average([team1['DF']*2,team1['MD'],team1['MO'],team1['TP'],team1['FI']])
		at = []
		base = base_distribution[st2][st1].copy()
		for i in range(4):
			at.append(effdiff(att2, def1))
		if at.count('A') == 4:
			base[0]-=5
			base[1]+=10
			base[2]+=10
		elif at.count('A') == 3:
			base[1]+=10
			base[2]+=5
		elif at.count('A') == 2:
			base[0]+=5
			base[1]+=5
		elif at.count('A') == 1:
			base[0]+=10
		elif at.count('A') == 0:
			base[0]+=15
			base[1]-=5
			base[2]-=10
		if team2['FI'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team2['FI'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team1['FI'] < 0.1:
			base[0]-=10
		elif team1['FI'] < 0.3:
			base[0]-=5
		if team2['MO'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team2['MO'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team1['MO'] < 0.1:
			base[0]-=10
		elif team1['MO'] < 0.3:
			base[0]-=5
		c2=choices([0,1,2], weights=base.values())[0]
		chances2+=c2
		g2 = 0
		for i in range(c2):
			go2 = round(np.average([team2['AT'],team2['MO'],team2['TP'],team2['FI']]), 3)
			go1 = round(np.average([team1['GK'],team1['MO'],team1['TP'],team1['FI']]), 3)
			if goleval(go2*.1, go1*.8) == 'f':
				g2+=1
				goals2+=1
		team1['MO'] = moralechanger(c1, c2, g1, g2, st1, team1['MO'])
		team2['MO'] = moralechanger(c2, c1, g2, g1, st2, team2['MO'])
	return (goals1, goals2)

def game(team1, team2):
	chances1 = 0
	chances2 = 0
	goals1 = 0
	goals2 = 0
	for turn in range(10):
		print("It's turn " + str(turn+1))
		st1 = input("Choose a strategy (F: Fitness-first; D: Defensive; C: Cautious, B: Balanced, A: Attacking, E:Extreme)")
		while st1 not in ['A', 'B', 'C', 'D', 'E', 'F']:
			st1 = raw_input("Please only input A, B, C, D, E, or F. (F: Fitness-first; D: Defensive; C: Cautious, B: Balanced, A: Attacking, E:Extreme)")
		st2 = stratchanger(goals2, goals1, turn, team2['FI'], team2['PE'])
		team1['FI'] -= normrand(0.06)*base_distribution[st1]['eff']
		team1['FI'] = fixval(team1['FI'])
		team2['FI'] -= normrand(0.06)*base_distribution[st2]['eff']
		team2['FI'] = fixval(team2['FI'])
		att1 = round(np.average([team1['AT']*2,team1['MD'],team1['MO'],team1['TP'],team1['FI']]), 3)
		def2 = round(np.average([team2['DF']*2,team2['MD'],team2['MO'],team2['TP'],team2['FI']]), 3)
		at = []
		base = base_distribution[st1][st2].copy()
		for i in range(4):
			at.append(effdiff(att1, def2))
		if at.count('A') == 4:
			base[0]-=5
			base[1]+=10
			base[2]+=10
		elif at.count('A') == 3:
			base[1]+=10
			base[2]+=5
		elif at.count('A') == 2:
			base[0]+=5
			base[1]+=5
		elif at.count('A') == 1:
			base[0]+=10
		elif at.count('A') == 0:
			base[0]+=15
			base[1]-=5
			base[2]-=10
		if team1['FI'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team1['FI'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team2['FI'] < 0.1:
			base[0]-=10
		elif team2['FI'] < 0.3:
			base[0]-=5
		if team1['MO'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team1['MO'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team2['MO'] < 0.1:
			base[0]-=10
		elif team2['MO'] < 0.3:
			base[0]-=5
		c1=choices([0,1,2], weights=base.values())[0]
		chances1+=c1
		g1 = 0
		for i in range(c1):
			go1 = round(np.average([team1['AT'],team1['MO'],team1['TP'],team1['FI']]), 3)
			go2 = round(np.average([team2['GK'],team2['MO'],team2['TP'],team2['FI']]), 3)
			if goleval(go1*.1, go2*.8) == 'f':
				g1+=1
				goals1+=1
		att2 = np.average([team2['AT']*2,team2['MD'],team2['MO'],team2['TP'],team2['FI']])
		def1 = np.average([team1['DF']*2,team1['MD'],team1['MO'],team1['TP'],team1['FI']])
		at = []
		base = base_distribution[st2][st1].copy()
		for i in range(4):
			at.append(effdiff(att2, def1))
		if at.count('A') == 4:
			base[0]-=5
			base[1]+=10
			base[2]+=10
		elif at.count('A') == 3:
			base[1]+=10
			base[2]+=5
		elif at.count('A') == 2:
			base[0]+=5
			base[1]+=5
		elif at.count('A') == 1:
			base[0]+=10
		elif at.count('A') == 0:
			base[0]+=15
			base[1]-=5
			base[2]-=10
		if team2['FI'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team2['FI'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team1['FI'] < 0.1:
			base[0]-=10
		elif team1['FI'] < 0.3:
			base[0]-=5
		if team2['MO'] < 0.1:
			base[1]-=10
			base[2]-=10
		elif team2['MO'] < 0.3:
			base[1]-=5
			base[2]-=5
		if team1['MO'] < 0.1:
			base[0]-=10
		elif team1['MO'] < 0.3:
			base[0]-=5
		c2=choices([0,1,2], weights=base.values())[0]
		chances2+=c2
		g2 = 0
		for i in range(c2):
			go2 = round(np.average([team2['AT'],team2['MO'],team2['TP'],team2['FI']]), 3)
			go1 = round(np.average([team1['GK'],team1['MO'],team1['TP'],team1['FI']]), 3)
			if goleval(go2*.1, go1*.8) == 'f':
				g2+=1
				goals2+=1
		team1['MO'] = moralechanger(c1, c2, g1, g2, st1, team1['MO'])
		team2['MO'] = moralechanger(c2, c1, g2, g1, st2, team2['MO'])
		print("You have created " + str(c1) + " " + str(chance[sp(c1)]) + " and have scored " + str(g1) + " " + str(goal[sp(g1)]) + ".")
		print("The opposing team created " + str(c2) + " " + str(chance[sp(c2)]) + " and scored " + str(g2) + " " + str(goal[sp(g2)]) + ".")
		print("The current score is " + str(goals1) + " to " + str(goals2) + ".")
	return (goals1, goals2)
