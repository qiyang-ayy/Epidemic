# -*- coding: utf-8 -*-
"""
Hospital Admission - Order to hospital
Consider hospital in models. Two hospital admission strategies: sequentiality and severity
As mentioned in epidemic.py, the recovery rate and mortality rate are different between in hospital and not in hospital.
* Isolation is not considered in the model, Only the patients in hospital are isolated from the outside world.

Models:
Model 4 - hospital sequentiality: hospital admission are decided by the order of being symptomatic.

Model 5 - hospital severity: hospital admission are decided by the order of possible time of getting infected.
Assumed the possible earliest infected day is that the earliest day of contact with infected person in the touch history
 list which saved in 'touch_history' attribution of nodes / persons. 

Inputs:
n - The number of nodes in network / the number of persons in society.
density - edges density.
d1 - the density of patients.
d2 - the density of asymptomatical virus carriers.
crowd_num - the range of the number of crowds/clusters.
r - rate of volume of the hospital over population of society.

Example:
n = 300, density = 2, d1 = 0.1, d2 = 0.1, crowd_num = [ 10, 20 ], r = 0.05.

Model 4 - No patients at all needs average 38 days and the average final number of recovery people and
dead people are respectively 260 and 40.

Model 5 - No patients at all needs average 21 days and the average final number of recovery people and
 dead people are 280 and 20 respectively.
Model 5 is a better way than chronological admission ( model 4 ).
comparing with model 5, the number of patients in model 6 drop even faster, at the same time the mortality rate
decrease.

Created on Thu May  7 23:00:51 2020
@author: Qiyang Ma
"""

import pycxsimulator
import random as rd
import matplotlib.pyplot as plt
import networkx as nx
import epidemic as ed

# basic parameters
n = 300
density = 2 # edges density
d1 = 0.1 # the density of patients
d2 = 0.1 # the density of asymptomatical virus carriers
crowd_num = [ 10, 20 ] # the range of the number of crowds/clusters
r = 0.05 # rate of volume of the hospital over population of society, assume hospital can accommodate 5% of the total humans
v = int( 300 * 0.05 ) # volume of the hospital


# Model 4
# hospital sequentiality - hospital admission are decided by the order of being symptomatic.
class hospital_sequentiality:
    def __init__( self, n = n, density = density, d1 = d1, d2 = d2, crowd_num = crowd_num, v = v ):
        self.n = n
        self.density = density
        self.d1 = d1
        self.d2 = d2
        self.crowd_num = crowd_num
        self.v = v
    
    def initialize( self ):
        global g, daynum, virus
        global num # the number of patients in hospitals
        daynum = 0
        virus = ed.virus()
        g = ed.createNodes( self.n, self.d1, self.d2, self.crowd_num, virus )
        g = ed.createEdges( g, daynum, self.density, virus )
        num = 0
        
    def observe( self ):
        global g, daynum, virus
        global num

        plt.cla()
        layout = nx.spring_layout( g )
        nx.draw( g, node_color = [ g.nodes[i][ 'color' ] for i in g.nodes ], node_size = 20, pos = layout )
        t = 'persons: ' + str( n ) + ', heathy: ' + str( virus.hnum ) + ', sick: ' + str( virus.pnum ) \
                + ', recovery: ' + str( virus.rnum ) + ', death: ' + str( virus.dnum ) + ' - day: ' + str( daynum ) 
        plt.title( t, fontsize = 10, fontfamily = 'Times New Roman' )
    
    def update( self ):
        global g, daynum, virus
        global num
        
        daynum += 1
        # update links
        g = ed.updateLinks( g, self.density, self.crowd_num )
        
        # update infection
        g = ed.updateInfected( g, virus )
        
        # not update order to hospital
        for i in g.nodes:
            if g.nodes[ i ][ 'state' ] >= 1:
                if num <= v:
                    g.nodes[ i ][ 'hospital' ] = 1
                    g.nodes[ i ][ 'isolation' ] = 1
                    g.nodes[ i ][ 'color' ] = 'k'
                    num += 1
        
        # update state
        g2 = g.copy()
        for i in g2.nodes:
            if g.nodes[ i ][ 'state' ] == 0:
                if g.nodes[ i ][ 'real' ] >= 1:
                    g.nodes[  i ][ 'real' ] += 1
                if rd.random() < virus.explicit_prob( g.nodes[ i ][ 'real' ] ):
                    g.nodes[ i ][ 'state' ] = g.nodes[ i ][ 'real' ]
                    g.nodes[ i ][ 'color' ] = 'r'
                    if num <= v:
                        g.nodes[ i ][ 'hospital' ] = 1
                        g.nodes[ i ][ 'isolation' ] = 1
                        g.nodes[ i ][ 'color' ] = 'k'
                        num += 1
            if g.nodes[ i ][ 'state' ] >= 1:
                if g.nodes[ i ][ 'hospital' ] == 1:
                    if rd.random() < virus.recovery_prob( g.nodes[i][ 'state' ], hos = 1 ):
                        g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                        g.nodes[i][ 'real' ] = 0.5
                        g.nodes[i][ 'color' ] = 'g'
                        g.nodes[i][ 'hospital' ] = 0
                        g.nodes[ i ][ 'isolation' ] = 0
                        num -= 1
                        virus.rnum += 1
                        virus.pnum -= 1
                        continue
                    if rd.random() < virus.death_prob( g.nodes[i][ 'state' ], hos = 1 ):
                        g.remove_node( i ) # The sick person has probability to die
                        num -= 1
                        virus.dnum += 1
                        virus.pnum -= 1
                        continue
                else:
                    if rd.random() < virus.recovery_prob( g.nodes[i][ 'state' ] ):
                        g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                        g.nodes[i][ 'real' ] = 0.5
                        g.nodes[i][ 'color' ] = 'g'
                        virus.rnum += 1
                        virus.pnum -= 1
                        continue
                    if rd.random() < virus.death_prob( g.nodes[i][ 'state' ] ):
                        g.remove_node( i ) # The sick person has probability to die  
                        virus.dnum += 1
                        virus.pnum -= 1
                        continue
                    if num <= v:
                        g.nodes[i][ 'hospital' ] = 1
                        g.nodes[ i ][ 'isolation' ] = 1
                        num += 1
    def run( self ):
        pycxsimulator.GUI().start( func = [ self.initialize, self.observe, self.update ] )


# Model 5
# hospital severity - hospital admission are decided by the order of possible time of getting infected.
class hospital_severity:
    def __init__( self, n = n, density = density, d1 = d1, d2 = d2, crowd_num = crowd_num, v = v ):
        self.n = n
        self.density = density
        self.d1 = d1
        self.d2 = d2
        self.crowd_num = crowd_num
        self.v = v
        
    def initialize( self ):
        global g, daynum, virus
        global num
        daynum = 0
        virus = ed.virus()
        g = ed.createNodes( self.n, self.d1, self.d2, self.crowd_num, virus )
        g = ed.createEdges( g, daynum, self.density, virus )
        num = 0

    def observe( self ):
        global g, daynum, virus
        global num    
        plt.cla()
        layout = nx.spring_layout( g )
        nx.draw( g, node_color = [ g.nodes[i][ 'color' ] for i in g.nodes ], node_size = 20, pos = layout )
        t = 'persons: ' + str( n ) + ', heathy: ' + str( virus.hnum ) + ', sick: ' + str( virus.pnum ) \
                + ', recovery: ' + str( virus.rnum ) + ', death: ' + str( virus.dnum ) + ' - day: ' + str( daynum ) 
        plt.title( t, fontsize = 10, fontfamily = 'Times New Roman' )
    
    def update( self ):
        global g, daynum, virus
        global num
        
        daynum += 1
        # update links
        g = ed.updateLinks( g, self.density, self.crowd_num )
        
        # update infection
        g = ed.updateInfected( g, virus )
    
        # update hospital order
        order = []
        g2 = g.copy()
        for i in g2.nodes:
            if g.nodes[ i ][ 'state' ] == 0:
                if g.nodes[ i ][ 'real' ] >= 1:
                    g.nodes[ i ][ 'real' ] += 1
                    if rd.random() < virus.explicit_prob( g.nodes[ i ][ 'real' ] ):
                        g.nodes[ i ][ 'state' ] = g.nodes[ i ][ 'hos_order' ]
                        order.append( ( i, g.nodes[i][ 'state' ]) )
            if g.nodes[ i ][ 'state' ] >= 1:
                for key in g.nodes[ i ][ 'touch_history' ]:
                    touches = set( g.nodes[ i ][ 'touch_history' ][ key ] )
                    for p in touches:
                        if p in g.nodes:
                            tmp = daynum % virus.hidden_day - key if daynum % virus.hidden_day > key \
                                    else virus.hidden_day - key + daynum % virus.hidden_day
                            g.nodes[ p ][ 'hos_order' ] = max( g.nodes[ p ][ 'hos_order' ], tmp )
                if g.nodes[i][ 'hospital' ] == 1:
                    g.nodes[i][ 'isolation' ] = 1
                    g.nodes[i][ 'color' ] = 'k'
                    if rd.random() < virus.recovery_prob( g.nodes[i][ 'state' ], hos = 1 ):
                        g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                        g.nodes[i][ 'real' ] = 0.5
                        g.nodes[i][ 'hospital' ] = 0
                        g.nodes[i][ 'color' ] = 'g'
                        g.nodes[i][ 'isolation' ] = 0
                        num -= 1
                        virus.rnum += 1
                        virus.pnum -= 1
                        continue
                    if rd.random() < virus.death_prob( g.nodes[i][ 'state' ], hos = 1 ):
                        g.remove_node( i ) # The sick person has probability to die
                        num -= 1
                        virus.dnum += 1
                        virus.pnum -= 1
                        continue
                else:
                    order.append( ( i, g.nodes[i][ 'state' ] ) )
                    if rd.random() < virus.recovery_prob( g.nodes[i][ 'state' ] ):
                        g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                        g.nodes[i][ 'real' ] = 0.5
                        g.nodes[i][ 'color' ] = 'g'
                        virus.rnum += 1
                        virus.pnum -= 1
                        continue
                    if rd.random() < virus.death_prob( g.nodes[i][ 'state' ] ):
                        g.remove_node( i ) # The sick person has probability to die
                        virus.dnum += 1
                        virus.pnum -= 1
                        continue
                g.nodes[ i ][ 'state' ] += 1
                g.nodes[ i ][ 'real' ] += 1
        
        #update order
        order = sorted( order, key = lambda x: x[1], reverse = True )
        n = 0
        while num <= v:
            i = order[ n ][0]
            if i in g.nodes:
                g.nodes[ i ][ 'hospital' ] = 1
                num += 1
            n += 1
    
    def run( self ):
        pycxsimulator.GUI().start( func = [ self.initialize, self.observe, self.update ] )