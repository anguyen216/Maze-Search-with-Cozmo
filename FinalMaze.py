#!/usr/bin/env python3

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps


class maze ():

    # startCoord - starting location, direction - facing direction
    # fixed order of navigation
    def __init__(self,startCoord, direction, robot):
        self.start = startCoord
        self.startDirection = direction
        self.robot = robot
        self.visitedRec = []
        self.deadendRec = []
        self.navorder = ["N","E","S","W","N"]
        
    # find NESW neighbors
    # Dr. Rosenthal's code
    def matneighbors(self,coordinate):
    	#array to hold the matneighbors
        n = []
        #the north neighbor
        if coordinate[1] != "1":
            n.append(coordinate[0]+str(int(coordinate[1])-1)) 
       #the east neighbor
        if coordinate[0] != "F":
            n.append(chr(ord(coordinate[0])+1)+coordinate[1]) 
        #the south neighbor
        if coordinate[1] != "6":
            n.append(coordinate[0]+str(int(coordinate[1])+1)) 
        #the west neighbor
        if coordinate[0] != "A":
            n.append(chr(ord(coordinate[0])-1)+coordinate[1]) 
        return n
    
    # coordinate - current location
    # find open path
    def accessible(self,coordinate):
        accessible = []
        for coord in self.matneighbors(coordinate):
            if coord not in self.walls()[coordinate]:
                accessible.append(coord)
        return accessible
       
    # dictionary of walls at each location 
    def walls(self):
        wall = {}
        wall["A1"] = ["B1"]
        wall["A2"] = ["A3"]
        wall["A3"] = ["A2","B3"]
        wall["A4"] = ["A5"]
        wall["A5"] = ["A4"]
        wall["A6"] = []
        wall["B1"] = ["A1"]
        wall["B2"] = ["C2"]
        wall["B3"] = ["A3"]
        wall["B4"] = ["C4","B5"]
        wall["B5"] = ["B4","C5","B6"]
        wall["B6"] = ["B5"]
        wall["C1"] = []
        wall["C2"] = ["B2","C3","D2"]
        wall["C3"] = ["C2","C4"]
        wall["C4"] = ["C3","B4","C5"]
        wall["C5"] = ["C4","B5"]
        wall["C6"] = []
        wall["D1"] = ["D2","E1"]
        wall["D2"] = ["D1","C2"]
        wall["D3"] = ["D4"]
        wall["D4"] = ["D3"]
        wall["D5"] = ["D6"]
        wall["D6"] = ["D5"]
        wall["E1"] = ["D1","E2"]
        wall["E2"] = ["E1","E3"]
        wall["E3"] = ["E2"]
        wall["E4"] = ["E5","F4"]
        wall["E5"] = ["E4","F5","E6"]
        wall["E6"] = ["E5"]
        wall["F1"] = []
        wall["F2"] = ["F3"]
        wall["F3"] = ["F2","F4"]
        wall["F4"] = ["F3","E4"]
        wall["F5"] = ["E5"]
        wall["F6"] = []
        return wall  
        
    def exit(self):
        return "F5"
    
    # first - current location, second - next location
    # get navigation direction
    # Dr. Rosenthal's code
    def getnavdirection(self, first, second):
        if first[0] < second[0]:
            return "E"
        if first[0] > second[0]:
            return "W"
        if first[1] < second[1]:
            return "S"
        if first[1] > second[1]:
            return "N"
    
    # path - array of current and next location
    # currdirection - current facing direction
    # Dr. Rosenthal's code
    def navigate_path(self, path, currdirection): 
        direction = currdirection
        index = 0
        while index < len(path) - 1:
            curr = path[index]
            next = path[index + 1]
            nextdirection = self.getnavdirection(curr, next)
            while direction != nextdirection:
                self.turn_right(self.robot)
                direction = self.navorder[self.navorder.index(direction) + 1]
            self.drive_straight(self.robot)
            index += 1
            
    # cozmo turns to 90 degrees to the right
    def turn_right(self,robot):
        robot.turn_in_place(degrees(-90)).wait_for_completed()
        
    # cozmo drives straight 150 mm at 100mmps
    def drive_straight(self,robot):
        robot.drive_straight(distance_mm(50),speed_mmps(25)).wait_for_completed()
     
    def start_explore(self):
        return self.explore(self.start,self.visitedRec,self.startDirection,self.deadendRec)
        
    def explore(self,currCoordinate,visited,cDirection,deadend):
        if currCoordinate not in visited:
            visited.append(currCoordinate)
		
        openPath = [] 
        for coord in self.accessible(currCoordinate):
            if coord not in visited:
                openPath.append(coord)
        
        #base case: dead end    
        # travel to coord in visited but not in deadend to find way out
        if openPath == []:
            deadend.append(currCoordinate)
            for coord in self.accessible(currCoordinate):
                if coord in visited and coord not in deadend:
                    self.navigate_path([currCoordinate,coord],cDirection)
                    self.explore(coord,visited,self.getnavdirection(currCoordinate,coord),deadend)
                    return False

        #if not deadend
        if openPath != []:
            for coord in openPath:
                #base case: found the exit
                if coord == self.exit():
                    self.navigate_path([currCoordinate,coord],cDirection)
                    visited.append(coord) 
                    direction = self.getnavdirection(currCoordinate,coord)
                    
                    while direction != "E":
                        self.turn_right(self.robot)
                        direction = self.navorder[self.navorder.index(direction)+1]
                    self.drive_straight(self.robot) 
                    return True
                    
                # not base case
                # depth-first search recurse
                else:
                    self.navigate_path([currCoordinate,coord],cDirection)
                    return self.explore(coord,visited,self.getnavdirection(currCoordinate,coord),deadend)

#search program - parameter: cozmo robot
# create m as an instance of maze class
#initialize A1 as starting location, South as facing direction when start
#  start the exploring process using given location and facing direction
def search_program (robot: cozmo.robot.Robot): 
    m = maze("A1","S",robot)
    m.start_explore()

# use_view = True allows user to see what cozmo sees while driving though the maze
cozmo.run_program(search_program, use_viewer=True)
