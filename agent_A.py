import math
import random
from collections import deque


# -*- coding: utf-8 -*-
memory = {} # dictionary mapping tuples to 1, if in dictionary, already visited...
maxdepth = 90
runningscore = 100
goal = ()
movenum = 0
currPath = []
firstmove = 0
pastlocations = {}
dictAdditions = 0

def nearCar(cur_position, cur_car_positions):

    x = cur_position[0]
    y = cur_position[1]
    for i in range(-2,3,1):
        for j in range(-2,3,1):
            if((x+i,y+j) in cur_car_positions):
                return 1
    return 0

def nearCoins(cur_position, cur_coin):

    ct = 0
    coords =[]
    x = cur_position[0]
    y = cur_position[1]
    for i in range(-1,2,1): #5 x 5 around coins
        for j in range(-1,2,1):
            if((x+i,y+j) in cur_coin):
                coords.append((x+i,y+j))
                return coords
                
    return coords

         

def findGoal(cur_map):
    for i in range(len(cur_map)):
        for j in range(len(cur_map[0])):
            if( cur_map[i][j] == 'goal'):
                return (i,j)
            
def findDistanceEuc(goal, nextMove):
    return abs(goal[0] - nextMove[0]) + abs(goal[1] - nextMove[1])


def coinDists(cur_location, coin_locations):
    sum =0
    for c in coin_locations:
        sum += findDistanceEuc(cur_location, c)

    return sum


def bfsSearch(cur_map, cur_pos, cur_coins, cur_car_positions, penalty_k):

    global currPath
    queue = deque()
    maxval = float('-inf')
    maxDir = "I"
    iter = 0
    maxpath = []
    maxDict= {}

    if(cur_pos[1] != len(cur_map[0])-1):
        queue.append([(cur_pos[0],cur_pos[1]+1),"S",runningscore,{},[cur_pos]])
    if(cur_pos[0]!=0):
        queue.append([(cur_pos[0]-1,cur_pos[1]),"A",runningscore,{},[cur_pos]])
    if(cur_pos[1]!=0):
        queue.append([(cur_pos[0],cur_pos[1]-1),"W",runningscore,{},[cur_pos]])
    if(cur_pos[0] != len(cur_map)-1):
        queue.append([(cur_pos[0]+1,cur_pos[1]),"D",runningscore,{},[cur_pos]])
    
    while(len(queue)!=0):

        layer = []
        while(len(queue)!=0):
            layer.append(queue.popleft())
    
        for node in layer:
            newScore = node[2]
            copy = node[4].copy()
            copy.append(node[0])
            copyDict = node[3].copy()

            if(node[0] in memory):
                if(newScore <= memory[node[0]]):# if ive been here before, but that path was better, no need to keep looking
                    continue

            if(node[0] in cur_car_positions or cur_map[node[0][0]][node[0][1]] == 'wall'): #if we would hit a car or wall, dont consider this part of the path
                continue

            memory[node[0]] = newScore 

            if(node[0] in cur_coins and (node[0] not in copyDict) ): # if we are on a coin, add to our score/// double claiming coins...
                newScore += 10
                copyDict[node[0]] = 1

            
            x = node[0][0]
            y = node[0][1]

            if(cur_map[node[0][0]][node[0][1]] == 'goal'):#goal is usually found with depth 40
                if(node[2] > maxval):
                    maxval = node[2]
                    maxDir = node[1]
                    maxpath = copy
                    maxDict= copyDict
                continue

            dist = 1.5 * penalty_k * findDistanceEuc(goal, node[0]) #heuristic
            
            if(newScore-dist > maxval and len(copyDict) != 0  ):#if the new score is better, and this path is attempting to find coins, we know this path doesnt end in the goal
                maxval = newScore-dist
                maxDir = node[1]
                maxpath = node[4]
                maxDict= copyDict
            
            if(iter == maxdepth):
                continue
                
            if(y!=0):
                queue.append([(x,y-1),node[1],newScore-penalty_k, copyDict,copy])
            if(y != len(cur_map[0])-1):
                queue.append([(x,y+1),node[1],newScore-penalty_k,copyDict,copy])
            if(x!=0):
                queue.append([(x-1,y), node[1],newScore-penalty_k,copyDict,copy])
            if(x != len(cur_map)-1):
                queue.append([(x+1,y),node[1],newScore-penalty_k,copyDict,copy])
            
        iter+=1
    
    currPath = maxpath.copy()
    return maxDir

def findDir(cur_pos, next_move):
    val = ""
    if(next_move[0] > cur_pos[0]):
        val = "D"
    if(next_move[0] < cur_pos[0]):
        val = "A"
    if(next_move[1] > cur_pos[1]):
        val = "S"
    if(next_move[1] < cur_pos[1]):
        val = "W"

    return val

    
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):
    
    global memory
    global runningscore
    global goal 
    global movenum
    global firstmove 
    global currPath
    global pastlocations
    global dictAdditions

    if(firstmove == 0):
        goal = findGoal(cur_map)
        firstmove = 1
    
    memory = {}
    
    val = ""

    if(movenum % 7 == 0):
        val = bfsSearch(cur_map,cur_position,cur_coins, cur_car_positions, penalty_k)
        movenum = 0
    else:
        if((movenum%7) + 1 < len(currPath)):
            location = currPath[(movenum%7) + 1]
            if(location not in cur_car_positions):
                val = findDir(cur_position, location)
            else:
                val = bfsSearch(cur_map,cur_position,cur_coins, cur_car_positions, penalty_k)
                movenum = 0
        else:
            val = bfsSearch(cur_map,cur_position,cur_coins, cur_car_positions, penalty_k)
            movenum = 0
    
    movenum+=1

    if(cur_position in pastlocations):
        pastlocations[cur_position] = pastlocations[cur_position]+1
        if(pastlocations[cur_position] >= 4):
            flag = True
            while(flag):
                randDir = random.choice([(cur_position[0]+1, cur_position[1]),(cur_position[0]-1, cur_position[1]),(cur_position[0], cur_position[1]+1),(cur_position[0], cur_position[1]-1)])
                if(cur_map[randDir[0]][randDir[1]]!= 'wall' and randDir not in cur_car_positions):
                    flag  = False
            val = findDir(cur_position, randDir)
            movenum = 0
            dictAdditions = 0
            pastlocations = {}
        else:
            dictAdditions+=1
    else:
        pastlocations[cur_position] = 1
        dictAdditions+=1
        if(len(pastlocations) > 20):
            dictAdditions = 0
            pastlocations = {}

    x = cur_position[0]
    y = cur_position[1]
    if(val == "W"):
        y-=1
    if(val == "S"):
        y+=1
    if(val == "A"):
        x-=1
    if(val == "D"):
        x+=1

    if((x,y) in cur_coins):
        runningscore+=10
    runningscore-=penalty_k
    if(runningscore < 0):
        runningscore = 0
    
    return val




    