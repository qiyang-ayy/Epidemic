# -*- coding: utf-8 -*-
"""
Epidemic attributes and infection in the dynamical networks
The assumed attributions of virus, update network/society and the epidemic information, record the newest epidemic data.

Class - virus

Inputs / assumptions:
hidden_day - the incumbation period of virus.
coef_recovery, coef_death, coef_infected - the parameters of recovery, death and infection probability distribution.

variable:
hnum - # of healthy people in network.
pnum - # of patients.
rnum - # of recovery persons.
dnum - # of death persons.

Functions:
recovery_prob - recovery probability of patients follows as normal distribution, e.g., norm( 30, 15 ).pdf( x )*20, x is ill days.
death_prob - death probability of patients follows as inverse distribution, e.g., 1 / ( 51-x ).
infect_prob - infection probability of healthy people follows as log distribution, e.g., log10( n+1 ), n is # of sick neighbours.
explicit_prob - symptoms manifest probability which follows as linear distribution, e.g. x/14 because the incubation of COVID19 ss 14 days.
free - 0: isolation; 1: no isolation because no symptoms when surpass the incubation period.
*: the reason why utilize those distribution and the picture of those distributions are shown in the introduction.pdf.


Dynamical Network:
d1, d2 - the density of patients, the density of asymptomatic virus carriers.
crowd_num - the range of the number of crowds/clusters in network.
daynum - number of days.
density - the edge density in the secondary clusters / crowds, the larger, the denser.

Attributions / variables:
state - explicit state of persons, 0: healthy or sick; 0.5: recovery; >=1, sick.
real - real state of persons, 0: healthy; 0.5: recovery; >=1: sick ( the larger, the worse ).
loc - the secondary clusters / crowds in network.
touch_history - record touch history with hidden days of the node (person).
isolation - whether isolation of the node ( person ).
iso_day - the number of isolation days.
hos - whether in hospital or not of the node ( person ).
hos_order - the order of accessing in hospital.
color - the color of nodes, 'b': healthy people; 'r': symptomatical patients; 'y': asymptomatical virus carriers; 'g': recovery people.

Functions:
createNotes - create nodes and add the attributions to the nodes in the network.
createEdges - create edges in the networks and record the touch history list for each nodes (persons).
updataLinks - update links between nodes for each day.
updateInfected - update infected persons in the network for each day.

Output:
GUI - display the dynamical network / society (g).
Including the number of healthy people, recovery people, dead peoplein the environment for each day. Finally, get the number of days
to make no infected people.

Created on Wed May  6 16:43:26 2020
@author: Qiyang Ma
"""

import pylab
import random as rd
import networkx as nx
from scipy.stats import norm
from collections import defaultdict

# Creat virus class
class virus:
    hnum, pnum, rnum, dnum = 0, 0, 0, 0
    def __init__( self, hidden_day = 14, recovery = [ 30, 15 ], death = 51, infected = 9  ):
        self.hidden_day = hidden_day
        self.coef_recovery = recovery
        self.coef_death = death
        self.coef_infected = infected
    
    def recovery_prob( self, x, hos = 0 ):
        rec = self.coef_recovery
        if hos:
            return norm( rec[0], rec[1] ).pdf( x ) * 30 # recovery probability in hospital
        else:
            return norm( rec[0], rec[1] ).pdf( x ) * 20 # recovery probability conform to normal distribution

    def death_prob( self, x, hos = 0 ):
        death = self.coef_death
        if hos:
            death += 5
            if x > death:
                x = death
            return 1 / ( death-x ) # death probability in hospital 
        else:
            if x > death:
                x = death
            return 1 / ( death-x ) # death probability conforms to inverse distribution

    def infection_prob( self, x ):
        infected = self.coef_infected
        if x > infected:
            x = infected
        return pylab.log10( 1+x ) # infection probability conforms to log distribution

    def explicit_prob( self, x ):
        return x / self.hidden_day
    
    def free( self, x ):
        if x >= self.hidden_day:
            return 0
        else:
            return 1


# Functions    
# create the network including nodes and edges to make up different groups in network/society
def createNodes( n, d1 = 0.1, d2 = 0.1, crowd_num = [ 10, 20 ], virus = virus() ):
    # Inputs:
    # n - # of nodes in network, means population in a society
    # d1, d2 - the density of patients, the density of asymptomatic virus carriers
    # crowd_num - the range of the number of crowds/clusters in network
    # Outputs:
    # g - network
    g = nx.Graph()
    numOfplace = pylab.choice( list( range( crowd_num[0], crowd_num[1] ) ) )    
    # create nodes ( persons ) and set their states in the network
    for i in range( n ):
        g.add_node( i )
        g.nodes[ i ][ 'state' ] = 1 if rd.random() < d1 else 0  # explicit state of persons
        g.nodes[ i ][ 'loc' ] = pylab.choice( numOfplace )
        g.nodes[ i ][ 'touch_history' ] = defaultdict( list ) # record touch history of the node (person)
        g.nodes[ i ][ 'isolation' ] = 0 # whether isolation
        g.nodes[ i ][ 'iso_day' ] = virus.hidden_day # the number of isolation days
        g.nodes[ i ][ 'hospital' ] = 0  # whether in hospital or not
        g.nodes[ i ][ 'hos_order' ] = 0 # the order of accessing in hospital
        if g.nodes[ i ][ 'state' ] == 0 and rd.random() < d2:
            g.nodes[ i ][ 'real' ] = 1  # real state of persons
        elif g.nodes[ i ][ 'state' ] == 1:
            g.nodes[ i ][ 'real' ] = 1
        else:
            g.nodes[ i ][ 'real' ] = 0
        if g.nodes[ i ][ 'state' ] == 0 and g.nodes[ i ][ 'real' ] == 1:
            g.nodes[ i ][ 'color' ] = 'y'
            virus.pnum += 1
        elif g.nodes[ i ][ 'state' ] == 1 and g.nodes[ i ][ 'real' ] == 1:
            g.nodes[ i ][ 'color' ] = 'r'
            virus.pnum += 1
        else:
            g.nodes[ i ][ 'color' ] = 'b'
            virus.hnum += 1
    return g

def createEdges( g, daynum, density = 2, virus = virus() ): 
    # Inputs:
    # g - network without edges
    # daynum - number of days
    # density - the edge density in the secondary clusters / crowds, the larger, the denser
    # Outputs:
    # g - network with new edges, and record touch nodes in this day
    placeDic = defaultdict( list )
    for i in g.nodes:
        if not g.nodes[ i ][ 'isolation' ]:
            place = g.nodes[ i ][ 'loc' ]
            placeDic[ place ].append( i )
    
    for key in placeDic:
        if len( placeDic[ key ] ) > 1:
            for i in range( len( placeDic[ key ] ) * density ):
                a, b = pylab.choice( placeDic[ key ], 2, replace = False )
                g.nodes[ a ][ 'touch_history' ][ daynum % virus.hidden_day ].append( b )
                g.nodes[ b ][ 'touch_history' ][ daynum % virus.hidden_day ].append( a )
                g.add_edge( a, b )
    return g

# update links (edges) to new groups and update the infection people
def updateLinks( g, density = 2, crowd_num = [ 10, 20 ] ):
    # Outputs:
    # network with new edges
    edges = list( g.edges() )
    g.remove_edges_from( edges )
    numOfplace = pylab.choice( list( range( crowd_num[0], crowd_num[1] ) ) )
    for i in g.nodes:
        g.nodes[ i ][ 'loc' ] = pylab.choice( numOfplace )
    g = createEdges( g, density )
    return g

def updateInfected( g, virus = virus() ):
    # Outputs:
    # network with new infected people
    for i in g.nodes:
        if g.nodes[ i ][ 'real' ] == 0:
            numOfsick = sum( [ 1 for j in list( g.neighbors( i ) ) if g.nodes[j][ 'real' ] >= 1 ] )
            if rd.random() < virus.infection_prob( numOfsick ):
                g.nodes[ i ][ 'real' ] = 1
                virus.pnum += 1
                virus.hnum -= 1
                if rd.random() < virus.explicit_prob( g.nodes[ i ][ 'real' ] ):
                    g.nodes[ i ][ 'state' ] = 1
                    g.nodes[ i ][ 'color' ] = 'r'
                else:
                    g.nodes[ i ][ 'state' ] = 0
                    g.nodes[ i ][ 'color' ] = 'y'
    return g