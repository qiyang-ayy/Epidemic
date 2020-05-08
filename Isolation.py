# -*- coding: utf-8 -*-
"""
Isolation Model
Isolation strategies include completely, partially and timely isolation.
The code can create the dynamical networks from those three methods to predict about the spread of COVID-19.
Test the best isolation method from those three models.

Models:
Model 1 - completely isolation: Everyone is immediately isolated from each other.

Model 2 - partially isolation: After sick, isolated from the outside world.

Model 3 - timely isolation: The patients and the people who are in his or her touch history list will be isolated as well.
The touch history list is saved in 'touch_history' attribution of nodes.

Inputs:
n - The number of nodes in network / the number of persons in society.
density - edges density.
d1 - the density of patients.
d2 - the density of asymptomatical virus carriers.
crowd_num - the range of the number of crowds/clusters.

Examples:
n = 300, density = 2, d1 = 0.1, d2 = 0.1, crowd_num = [ 10, 20 ].

Model 1 - epidemic can be effectively controlled but will large economic losses.
The average final number of rest healthy people, recovery people, dead people are respectively
230, 63 and 7. No patients at all need average 14 days.

Model 2 - no valid method, nearly 100% people in the network are infected.
The average final number of rest healthy people, recovery people, dead people are respectively
3, 267 and 30. No patients at all need average 24 days.
Even though little sick persons in network, finally nearly 100% people get infected.

Model 3 - Effective and efficient isolation method, also ensure society works.
The average final number of rest healthy people, recovery people, dead people are respectively 168, 
122 and 10. No patients at all need average 18 days.
Mostly important, few people who are not suspected to infected and recovery humans can continue
to work during the isolation period!

Created on Wed May  6 17:35:10 2020
@author: Qiyang Ma
"""

import pycxsimulator
import random as rd
import matplotlib.pyplot as plt
import networkx as nx
import epidemic as ed

# basic parameters
n = 300 # The number of nodes
density = 2 # edges density
d1 = 0.1 # the density of patients
d2 = 0.1 # the density of asymptomatical virus carriers
crowd_num = [ 10, 20 ] # the range of the number of crowds/clusters

# Model 1
# Completely isolation - Everyone is immediately isolated from each other
class complete_isolation:
    def __init__( self, n = n, density = density, d1 = d1, d2 = d2, crowd_num = crowd_num ):
        self.n = n
        self.density = density
        self.d1 = d1
        self.d2 = d2
        self.crowd_num = crowd_num
    
    def initialize( self ):
        global g, daynum, virus        
        daynum = 0
        g = nx.Graph()
        virus = ed.virus()
        g = ed.createNodes( self.n, self.d1, self.d2, self.crowd_num, virus )
        g = ed.createEdges( g, daynum, self.density, virus )
    
    def observe( self ):
        global g, daynum, virus        
        plt.cla()
        layout = nx.spring_layout( g )
        nx.draw( g, node_color = [ g.nodes[i][ 'color' ] for i in g.nodes ], node_size = 20, pos = layout )
        t = 'persons: ' + str( self.n ) + ', heathy: ' + str( virus.hnum ) + ', sick: ' + str( virus.pnum ) \
                + ', recovery: ' + str( virus.rnum ) + ', death: ' + str( virus.dnum ) + ' - day: ' + str( daynum ) 
        plt.title( t, fontsize = 10, fontfamily = 'Times New Roman' )
    
    def update( self ):
        global g, daynum, virus
        daynum += 1
        
        for i in g.nodes:
            for j in list( g.neighbors( i ) ):
                g.remove_edge( i, j )
            if g.nodes[i][ 'real' ] >= 1:
                g.nodes[i][ 'state' ] = g.nodes[i][ 'real' ]
                g.nodes[i][ 'real'] = 0
        g2 = g.copy()
        for i in g2.nodes:
            if g.nodes[i][ 'state' ] >= 1:
                g.nodes[i][ 'state' ] += 1
                if rd.random() < virus.recovery_prob( g.nodes[i][ 'state' ] ):
                    g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                    g.nodes[i][ 'color' ] = 'g'
                    virus.rnum += 1
                    virus.pnum -= 1
                    continue
                if rd.random() < virus.death_prob( g.nodes[i][ 'state' ] ):
                    g.remove_node( i ) # The sick person has probability to die
                    virus.dnum += 1
                    virus.pnum -= 1
                    continue
    
    def run( self ):
        pycxsimulator.GUI().start( func = [ self.initialize, self.observe, self.update ] )


# Model 2
# Partially isolation - after he or she sicks, isolated from the outside world
class partial_isolation:
    def __init__( self, n = n, density = density, d1 = d1, d2 = d2, crowd_num = crowd_num ):
        self.n = n
        self.density = density
        self.d1 = d1
        self.d2 = d2
        self.crowd_num = crowd_num
    
    def initialize( self ):
        global g, daynum, virus        
        daynum = 0
        g = nx.Graph()
        virus = ed.virus()
        g = ed.createNodes( self.n, self.d1, self.d2, self.crowd_num, virus )
        g = ed.createEdges( g, daynum, self.density, virus )
    
    def observe( self ):
        global g, daynum, virus        
        plt.cla()
        layout = nx.spring_layout( g )
        nx.draw( g, node_color = [ g.nodes[ i ][ 'color' ] for i in g.nodes ], node_size = 20, pos = layout )
        t = 'persons: ' + str( n ) + ', heathy: ' + str( virus.hnum ) + ', sick: ' + str( virus.pnum ) \
                + ', recovery: ' + str( virus.rnum ) + ', death: ' + str( virus.dnum ) + ' - day: ' + str( daynum ) 
        plt.title( t, fontsize = 10, fontfamily = 'Times New Roman' )
    
    def update( self ):
        global g, daynum, virus
        daynum += 1
        
        #update links
        g = ed.updateLinks( g, self.density, self.crowd_num )
        
        # Update infection
        g = ed.updateInfected( g, virus )
    
        
        g2 = g.copy()
        # Update isolation and epidemic information
        for i in g2.nodes:
            if g.nodes[ i ][ 'state' ] == 0:
                for j in list( g.neighbors( i ) ):
                    if g.nodes[ j ][ 'state' ] >= 1:
                        g.remove_edge( i, j  )
                if g.nodes[ i ][ 'real' ] >= 1:
                    g.nodes[i][ 'real' ] += 1
                if rd.random() < virus.explicit_prob( g.nodes[ i ][ 'real' ] ):
                    g.nodes[ i ][ 'state' ] = g.nodes[ i ][ 'real' ]
                    g.nodes[ i ][ 'color' ] = 'r'
            elif g.nodes[ i ][ 'state' ] >= 1:
                g.nodes[ i ][ 'isolation' ] = 1
                if rd.random() < virus.recovery_prob( g.nodes[ i ][ 'real' ] ):
                    g.nodes[ i ][ 'state' ] = 0.5 # The sick person recovered
                    g.nodes[ i ][ 'real' ] = 0.5
                    g.nodes[ i ][ 'color' ] = 'g'
                    g.nodes[ i ][ 'isolation' ] = 0
                    virus.rnum += 1
                    virus.pnum -= 1
                    continue
                if rd.random() < virus.death_prob( g.nodes[ i ][ 'real' ] ):
                    g.remove_node( i ) # The sick person has probability to die
                    virus.dnum += 1
                    virus.pnum -= 1
                    continue
                g.nodes[i][ 'state' ] += 1
                g.nodes[i][ 'real' ] += 1
    
    def run( self ):
        pycxsimulator.GUI().start( func = [ self.initialize, self.observe, self.update ] )


# Model 3
# timely isolation - The patients and the people who are in his or her touch history list will be isolated as well.
class time_isolation:
    def __init__( self, n = n, density = density, d1 = d1, d2 = d2, crowd_num = crowd_num ):
        self.n = n
        self.density = density
        self.d1 = d1
        self.d2 = d2
        self.crowd_num = crowd_num
        
    def initialize( self ):
        global g, daynum, virus
        daynum = 0
        virus = ed.virus()
        
        g = nx.Graph()
        g = ed.createNodes( self.n, self.d1, self.d2, self.crowd_num, virus )
        g = ed.createEdges( g, daynum, self.density, virus  )
    
    def observe( self ):
        global g, daynum, virus    
        plt.cla()
        layout = nx.spring_layout( g )
        nx.draw( g, node_color = [ g.nodes[i][ 'color' ] for i in g.nodes ], node_size = 20, pos = layout )
        t = 'persons: ' + str( n ) + ', heathy: ' + str( virus.hnum ) + ', sick: ' + str( virus.pnum ) \
                + ', recovery: ' + str( virus.rnum ) + ', death: ' + str( virus.dnum ) + ' - day: ' + str( daynum ) 
        plt.title( t, fontsize = 10, fontfamily = 'Times New Roman' )
    
    def update( self ):
        global g, daynum, virus       
        daynum += 1
        
        # update links
        g = ed.updateLinks( g, self.density, self.crowd_num )
        
        # update infection
        g = ed.updateInfected( g, virus )
        
        # update isolation and epidemic information
        g2 = g.copy()
        for i in g2.nodes:
            if g.nodes[ i ][ 'state' ] == 0:
                if g.nodes[ i ][ 'real' ] >= 1:
                    g.nodes[i][ 'real' ] += 1
                    g.nodes[i][ 'iso_day' ] += 1
                if rd.random() < virus.explicit_prob( g.nodes[ i ][ 'real' ] ):
                    g.nodes[ i ][ 'state' ] = 1
                    g.nodes[ i ][ 'color' ] = 'r'
                if g.nodes[ i ][ 'real' ] == 0 and g.nodes[ i ][ 'isolation' ] == 1:
                    g.nodes[ i ][ 'iso_day' ] += 1
                    g.nodes[ i ][ 'isolation' ] = virus.free( g.nodes[ i ][ 'iso_day' ] )
            if g.nodes[ i ][ 'state' ] >= 1:
                g.nodes[ i ][ 'isolation' ] = 1
                if g.nodes[ i ][ 'state' ] == 1:
                    for key in g.nodes[ i ][ 'touch_history' ]:
                        touches = set( g.nodes[ i ][ 'touch_history' ][ key ] )
                        for p in touches:
                            if p in g.nodes:
                                if g.nodes[ p ][ 'real' ] != 0.5:
                                    g.nodes[ p ][ 'isolation' ] = 1
                                    tmp = daynum % virus.hidden_day - key if daynum % virus.hidden_day > key \
                                                else virus.hidden_day - key + daynum % virus.hidden_day
                                    g.nodes[ p ][ 'iso_day' ] = min( g.nodes[ p ][ 'iso_day' ], tmp )
                if rd.random() < virus.recovery_prob( g.nodes[i][ 'real' ] ):
                    g.nodes[i][ 'state' ] = 0.5 # The sick person recovered
                    g.nodes[i][ 'real' ] = 0.5
                    g.nodes[i][ 'isolation' ] = 0
                    g.nodes[i][ 'color' ] = 'g'
                    virus.rnum += 1
                    virus.pnum -= 1
                    continue
                if rd.random() < virus.death_prob( g.nodes[i][ 'real' ] ):
                    g.remove_node( i ) # The sick person has probability to die  
                    virus.dnum += 1
                    virus.pnum -= 1
                    continue
                g.nodes[ i ][ 'state' ] += 1
                g.nodes[ i ][ 'real' ] += 1
    
    def run( self ):
        pycxsimulator.GUI().start( func = [ self.initialize, self.observe, self.update ] )