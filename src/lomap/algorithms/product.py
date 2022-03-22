# Copyright (C) 2012-2015, Alphan Ulusoy (alphan@bu.edu)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import networkx as nx
import itertools as it
from ..classes.model import Model
from ..classes.ts import Ts
from ..classes.markov import Markov
import sys
import logging

# Logger configuration
logger = logging.getLogger(__name__)
#logger.addHandler(logging.NullHandler())

__all__ = ['ts_times_ts', 'ts_times_buchi', 'ts_times_fsa', 'markov_times_markov', 'markov_times_fsa']


def ts_times_fsa(ts, fsa):

	# Create the product_model
	product_model = Model()

	# Iterate over initial states of the TS
	init_states = []
	for init_ts in ts.init.keys():
		init_prop = ts.g.node[init_ts].get('prop',set())
		# Iterate over the initial states of the FSA
		for init_fsa in fsa.init.keys():
			# Add the initial states to the graph and mark them as initial
			for act_init_fsa in fsa.next_states_of_fsa(init_fsa, init_prop):
				init_state = (init_ts, act_init_fsa)
				init_states.append(init_state)
				product_model.init[init_state] = 1
				product_model.g.add_node(init_state, {'prop':init_prop, 'label':"%s\\n%s" % (init_state,list(init_prop))})
				if act_init_fsa in fsa.final:
					product_model.final.add(init_state)

	# Add all initial states to the stack
	stack = []
	for init_state in init_states:
		stack.append(init_state)

	# Consume the stack
	while(stack):
		cur_state = stack.pop()
		ts_state = cur_state[0]
		fsa_state = cur_state[1]
	
		for ts_next in ts.next_states_of_wts(ts_state, traveling_states = False):
			ts_next_state = ts_next[0]
			ts_next_prop = ts.g.node[ts_next_state].get('prop',set())
			weight = ts_next[1]
			control = ts_next[2]
			for fsa_next_state in fsa.next_states_of_fsa(fsa_state, ts_next_prop):
				next_state = (ts_next_state, fsa_next_state)
				#print "%s -%d-> %s" % (cur_state, weight, next_state)
	
				if(next_state not in product_model.g):
					 next_prop = ts.g.node[ts_next_state].get('prop',set())
	
					 # Add the new state
					 product_model.g.add_node(next_state, {'prop': next_prop, 'label': "%s\\n%s" % (next_state, list(next_prop))})
	
					 # Add transition w/ weight
					 product_model.g.add_edge(cur_state, next_state, attr_dict = {'weight':weight, 'control':control})
	
					 # Mark as final if final in fsa
					 if fsa_next_state in fsa.final:
						 product_model.final.add(next_state)
	
					 # Continue search from next state
					 stack.append(next_state)
	
				elif(next_state not in product_model.g[cur_state]):
					product_model.g.add_edge(cur_state, next_state, attr_dict = {'weight':weight, 'control':control})

	return product_model

def ts_times_buchi(ts, buchi):

	# Create the product_model
	product_model = Model()

	# Iterate over initial states of the TS
	init_states = []
	for init_ts in ts.init.keys():
		init_prop = ts.g.node[init_ts].get('prop',set())
		# Iterate over the initial states of the FSA
		for init_buchi in buchi.init.keys():
			# Add the initial states to the graph and mark them as initial
			for act_init_buchi in buchi.next_states_of_buchi(init_buchi, init_prop):
				init_state = (init_ts, act_init_buchi)
				init_states.append(init_state)
				product_model.init[init_state] = 1
				product_model.g.add_node(init_state, {'prop':init_prop, 'label':"%s\\n%s" % (init_state,list(init_prop))})
				if act_init_buchi in buchi.final:
					product_model.final.add(init_state)

	# Add all initial states to the stack
	stack = []
	for init_state in init_states:
		stack.append(init_state)

	# Consume the stack
	while(stack):
		cur_state = stack.pop()
		ts_state = cur_state[0]
		buchi_state = cur_state[1]
	
		for ts_next in ts.next_states_of_wts(ts_state, traveling_states = False):
			ts_next_state = ts_next[0]
			ts_next_prop = ts.g.node[ts_next_state].get('prop',set())
			weight = ts_next[1]
			control = ts_next[2]
			for buchi_next_state in buchi.next_states_of_buchi(buchi_state, ts_next_prop):
				next_state = (ts_next_state, buchi_next_state)
				#print "%s -%d-> %s" % (cur_state, weight, next_state)
	
				if(next_state not in product_model.g):
					 next_prop = ts.g.node[ts_next_state].get('prop',set())
	
					 # Add the new state
					 product_model.g.add_node(next_state, {'prop': next_prop, 'label': "%s\\n%s" % (next_state, list(next_prop))})
	
					 # Add transition w/ weight
					 product_model.g.add_edge(cur_state, next_state, attr_dict = {'weight':weight, 'control':control})
	
					 # Mark as final if final in buchi
					 if buchi_next_state in buchi.final:
						 product_model.final.add(next_state)
	
					 # Continue search from next state
					 stack.append(next_state)
	
				elif(next_state not in product_model.g[cur_state]):
					product_model.g.add_edge(cur_state, next_state, attr_dict = {'weight':weight, 'control':control})

	return product_model

def ts_times_ts(ts_tuple):

	# Initial state label is the tuple of initial states' labels
	# NOTE: We assume deterministic TS (that's why we pick [0])
	assert all(map(lambda ts: True if len(ts.init) == 1 else False, ts_tuple))
	init_state = tuple(map(lambda ts: ts.init.keys()[0], ts_tuple))
	product_ts = Ts()
	product_ts.init[init_state] = 1

	# Props satisfied at init_state is the union of props
	# For each ts, get the prop of init state or empty set
	init_prop = map(lambda ts: ts.g.node[ts.init.keys()[0]].get('prop',set()), ts_tuple)

	# This makes each set in the list a new argument and takes the union
	init_prop = set.union(*init_prop)

	# Finally, add the state
	product_ts.g.add_node(init_state, {'prop':init_prop, 'label':"%s\\n%s" % (init_state,list(init_prop))})

	# Start depth first search from the initial state
	stack=[]
	stack.append(init_state)

	while(stack):
		cur_state = stack.pop()
		# Actual source states of traveling states
		source_state = tuple(map(lambda q: q[0] if type(q) == tuple else q, cur_state))
		# Time spent since actual source states
		time_spent = tuple(map(lambda q: q[2] if type(q) == tuple else 0, cur_state))

		# Iterate over all possible transitions
		for tran_tuple in it.product(*map(lambda t,q: t.next_states_of_wts(q), ts_tuple, cur_state)):
			# tran_tuple is a tuple of m-tuples (m: size of ts_tuple)

			# First element of each tuple: next_state
			# Second element of each tuple: time_left
			next_state = tuple([t[0] for t in tran_tuple])
			time_left = tuple([t[1] for t in tran_tuple])
			control = tuple([t[2] for t in tran_tuple])

			# Min time until next transition
			w_min = min(time_left)

			# Next state label. Singleton if transition taken, tuple if traveling state
			next_state = tuple(map(lambda ss, ns, tl, ts: (ss,ns,w_min+ts) if w_min < tl else ns, source_state, next_state, time_left, time_spent))

			# Add node if new
			if(next_state not in product_ts.g):
				 # Props satisfied at next_state is the union of props
				 # For each ts, get the prop of next state or empty set
				 # Note: we use .get(ns, {}) as this might be a travelling state
				 next_prop = map(lambda ts,ns: ts.g.node.get(ns,{}).get('prop',set()), ts_tuple, next_state)
				 next_prop = set.union(*next_prop)

				 # Add the new state
				 product_ts.g.add_node(next_state, {'prop': next_prop, 'label': "%s\\n%s" % (next_state, list(next_prop))})

				 # Add transition w/ weight
				 product_ts.g.add_edge(cur_state, next_state, attr_dict = {'weight':w_min, 'control':control})
				 #print "%s -%d-> %s (%s)" % (cur_state,w_min,next_state,next_prop)
				 # Continue dfs from ns
				 stack.append(next_state)

			# Add tran w/ weight if new
			elif(next_state not in product_ts.g[cur_state]):
				 product_ts.g.add_edge(cur_state, next_state, attr_dict = {'weight':w_min, 'control':control})
				 #print "%s -%d-> %s" % (cur_state,w_min,next_state)

	# Return ts_1 x ts_2 x ...
	return product_ts

def flatten_tuple(t):
	flat_tuple = ()
	for item in t:
		if isinstance(item, tuple):
			flat_tuple += item
		else:
			flat_tuple += (item,)
	return flat_tuple

def markov_times_markov(markov_tuple):

	# This results in an Mdp
	mdp = Markov()
	mdp.init = dict()

	# Stack for depth first search
	stack=[]

	# Find the initial states of the MDP
	for init_state in it.product(*map(lambda m: m.init.keys(), markov_tuple)):
		
		# Find initial probability and propositions of this state
		init_prob = reduce(lambda x,y: x*y, map(lambda m, s: m.init[s], markov_tuple, init_state))
		init_prop = reduce(lambda x,y: x|y, map(lambda m, s: m.g.node[s].get('prop',set()), markov_tuple, init_state))

		flat_init_state = flatten_tuple(init_state)

		# Set the initial probability of this state
		mdp.init[flat_init_state] = init_prob
		# Add the state to the graph
		mdp.g.add_node(flat_init_state, {'prop':init_prop, 'label':r'%s\n%.2f\n%s' % (flat_init_state,init_prob,list(init_prop))})
		# Start depth first search from the initial states
		stack.append(init_state)

	while(stack):
		cur_state = stack.pop()

		# Actual source states of traveling states
		source_state = tuple(map(lambda q: q[0] if isinstance(q, tuple) and len(q)==3 and isinstance(q[2], (int, float, long)) else q, cur_state))
		# Time spent since actual source states
		time_spent = tuple(map(lambda q: q[2] if isinstance(q, tuple) and len(q)==3 and isinstance(q[2], (int, float, long)) else 0, cur_state))

		# Iterate over all possible transitions
		for tran_tuple in it.product(*map(lambda t,q: t.next_states_of_markov(q), markov_tuple, cur_state)):
			# tran_tuple is a tuple of m-tuples (m: size of ts_tuple)

			# First element of each tuple: next_state
			# Second element of each tuple: time_left
			# Third element of each tuple: control	
			# Forth element of each tuple: tran_prob
			next_state = tuple([t[0] for t in tran_tuple])
			time_left = tuple([t[1] for t in tran_tuple])
			control = tuple([t[2] for t in tran_tuple])
			prob = tuple([t[3] for t in tran_tuple])

			# Min time until next transition
			w_min = min(time_left)
			tran_prob = reduce(lambda x,y: x*y, prob)

			# Next state label. Singleton if transition taken, tuple if traveling state
			next_state = tuple(map(lambda ss, ns, tl, ts: (ss,ns,w_min+ts) if w_min < tl else ns, source_state, next_state, time_left, time_spent))

			# Compute flat labels
			flat_cur_state = flatten_tuple(cur_state)
			flat_next_state = flatten_tuple(next_state)
			flat_control = flatten_tuple(control)

			# Add node if new
			if(flat_next_state not in mdp.g):
				 # Props satisfied at next_state is the union of props
				 # For each ts, get the prop of next state or empty set
				 # Note: we use .get(ns, {}) as this might be a travelling state
				 next_prop = map(lambda m,ns: m.g.node.get(ns,{}).get('prop',set()), markov_tuple, next_state)
				 next_prop = set.union(*next_prop)

				 # Add the new state
				 mdp.g.add_node(flat_next_state, {'prop': next_prop, 'label': "%s\\n%s" % (flat_next_state, list(next_prop))})

				 # Add transition w/ weight
				 mdp.g.add_edge(flat_cur_state, flat_next_state, attr_dict = {'weight':w_min, 'control':flat_control, 'prob':tran_prob})
				 #print "%s -%d-> %s (%s)" % (cur_state,w_min,next_state,next_prop)
				 # Continue dfs from ns
				 stack.append(next_state)

			# Add tran w/ weight if new
			elif(flat_next_state not in mdp.g[flat_cur_state]):
				mdp.g.add_edge(flat_cur_state, flat_next_state, attr_dict = {'weight':w_min, 'control':flat_control, 'prob':tran_prob})
				#print "%s -%d-> %s" % (cur_state,w_min,next_state)

	# Return m1 x m2 x ...
	return mdp


def markov_times_fsa(markov, fsa):

	# Create the product_model
	p = Markov()
	p.name = 'Product of %s and %s' % (markov.name, fsa.name)
	p.init = {}
	p.final = set()

	# Stack for depth first search
	stack = []
	# Iterate over initial states of the markov model
	for init_markov in markov.init.keys():
		init_prop = markov.g.node[init_markov].get('prop',set())
		# Iterate over the initial states of the FSA
		for init_fsa in fsa.init.keys():
			# Add the initial states to the graph and mark them as initial
			for act_init_fsa in fsa.next_states_of_fsa(init_fsa, init_prop):
				init_state = (init_markov, act_init_fsa)
				# Flatten state label
				flat_init_state = flatten_tuple(init_state)
				# Probabilities come from the markov model as FSA is deterministic
				p.init[flat_init_state] = markov.init[init_markov]
				p.g.add_node(flat_init_state, {'prop':init_prop, 'label':r'%s\n%.2f\n%s' % (flat_init_state,p.init[flat_init_state],list(init_prop))})
				if act_init_fsa in fsa.final:
					p.final.add(flat_init_state)
				# Add this initial state to stack
				stack.append(init_state)

	# Consume the stack
	while(stack):
		cur_state = stack.pop()
		flat_cur_state = flatten_tuple(cur_state)
		markov_state = cur_state[0]
		fsa_state = cur_state[1]
	
		for markov_next in markov.next_states_of_markov(markov_state, traveling_states = False):
			markov_next_state = markov_next[0]
			markov_next_prop = markov.g.node[markov_next_state]['prop']
			weight = markov_next[1]
			control = markov_next[2]
			prob = markov_next[3]
			for fsa_next_state in fsa.next_states_of_fsa(fsa_state, markov_next_prop):
				next_state = (markov_next_state, fsa_next_state)
				flat_next_state = flatten_tuple(next_state)
				#print "%s -%d-> %s" % (cur_state, weight, next_state)
	
				if(flat_next_state not in p.g):
					 next_prop = markov.g.node[markov_next_state].get('prop',set())
	
					 # Add the new state
					 p.g.add_node(flat_next_state, {'prop': next_prop, 'label': "%s\\n%s" % (flat_next_state, list(next_prop))})
	
					 # Add transition w/ weight and prob
					 p.g.add_edge(flat_cur_state, flat_next_state, attr_dict = {'weight':weight, 'control':control, 'prob':prob})
	
					 # Mark as final if final in fsa
					 if fsa_next_state in fsa.final:
						 p.final.add(flat_next_state)
	
					 # Continue search from next state
					 stack.append(next_state)
	
				elif(flat_next_state not in p.g[flat_cur_state]):
					p.g.add_edge(flat_cur_state, flat_next_state, attr_dict = {'weight':weight, 'control':control, 'prob':prob})

	return p
