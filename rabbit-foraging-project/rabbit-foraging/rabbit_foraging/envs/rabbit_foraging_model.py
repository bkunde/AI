import random
import math
import numpy as np
import copy

class RabbitForagingState:
    """Map of N size, represented by a list of list. 0 is an empty cell, 1 is a tree, 2 is a rock, 3 is water, 4 is a food bush, 5 is a burrow, 6 is a rabbit, 7 is an eaten bush, """
    def __init__(self, size=5):
        #self._map = [[0 for i in range(size)] for j in range(size)]
        self._map = np.array([[0 for i in range(size)] for j in range(size)], np.int8)
        #self._rabbit = (None, None, 0)
        self._rabbit = np.array([-1, -1, 0], np.int8)
        self._burrow = (None, None)
        self._size = size
        return 

    @property
    def map(self):
        return self._map

    @property
    def size(self):
        return self._size

    @property
    def rabbit(self):
        return self._rabbit
    
    @rabbit.setter
    def rabbit(self, rabbit):
        self._rabbit = rabbit

    @property
    def observation(self):
        #return self
        return {"map": self._map, "rabbit": self._rabbit, "size": self._size}
    #(self, self._map, self._rabbit)

    @observation.setter
    def observation(self, value):
        #self._map = value.map
        #self._rabbit = value.rabbit
        self._map = value["map"]
        self._rabbit = value["rabbit"]
        return 

    def obsToState(self):
        return self

    def randomize(self, seed=None):
        if seed is not None:
            np.random.seed(seed)

        #Place Trees
        trees = random.randint(int(self._size/2), self._size)
        for tree in range(trees):
            coords = self.getRandomRowCol()
            while (self._map[coords[0]][coords[1]] != 0):
                coords = self.getRandomRowCol()
            self._map[coords[0]][coords[1]] = 1

        """Place Rocks"""
        rocks = random.randrange(self._size)
        for rock in range(rocks):
            coords = self.getRandomRowCol()
            while (self._map[coords[0]][coords[1]] != 0):
                coords = self.getRandomRowCol()
            self._map[coords[0]][coords[1]] = 2

        """Place River"""
        river = random.randrange(2)
        start = self.getRandomRowCol()
        if river == 0: #N-S
            start = start[1]
            for col in range(self._size)[::-1]:
                self._map[col][start] = 3
        if river == 1: #E-W
            start = start[0]
            for row in range(self._size):
                self._map[start][row] = 3

        #Place Food bushes
        bushes = random.randint(2, int(self._size/2))
        for bush in range(bushes):
            coords = self.getRandomRowCol()
            while (self._map[coords[0]][coords[1]] != 0):
                coords = self.getRandomRowCol()
            self._map[coords[0]][coords[1]] = 4

        #Place burrow
        coords = self.getRandomRowCol()
        while (self._map[coords[0]][coords[1]] != 0):
            coords = self.getRandomRowCol()
        self._map[coords[0]][coords[1]] = 5
        self._burrow = (coords[0], coords[1])
        #Set rabbit at burrow
        #self._rabbit = (coords[0], coords[1], 0)
        self._rabbit[0] = coords[0]
        self._rabbit[1] = coords[1]
        return self._map

    def getBurrow(self):
        return self._burrow

    def getRandomRowCol(self):
        row = random.randrange(self._size)
        col = random.randrange(self._size)
        return(row, col)

    def __str__(self):
        s = "\n+"+"---"*(self._size+3)+"+"
        for row in self._map[::-1]:
            s += "\n|"
            for col in row:
                s += f" {col} |"
        s += "\n+"+"---"*(self._size+3)+"+"
        s += f"\n{self._rabbit}"
        return s

                
if __name__ == '__main__':
    state = RabbitForagingState()
    print(state)
    state.randomize()
    print(state)


class RabbitForagingModel:
    
    def ACTIONS(state):
        """
        0: Move down
        1: Move up
        2: Move right
        3: Move left
        4: Eat Food
        """
        actions = [0,1,2,3]
        rabbit = state["rabbit"]
        stateMap = state["map"]
        size = state["size"]
        #rabbit = state.rabbit
        if rabbit[0] == 0: #bottom row
            if rabbit[1] == 0: #right corner
                #obstacle above rabbit
                if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                    actions = [3]
                #obstacle to the left of rabbit
                elif stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                    actions = [1]
                else:
                    actions = [1,3]
            elif rabbit[1] == size-1: #left corner
                #obstacle above rabbit
                if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                    actions = [2]
                #obstacle to the right of rabbit
                elif stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                    actions = [1]
                else:
                    actions = [1,2]
            else:
                #obstacle above rabbit
                if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                    actions = [2,3]
                #obstacle to the left of rabbit
                elif stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                    actions = [1,2]
                #obstacle to the right of rabbit
                elif stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                    actions = [1,3]
                else:
                    actions = [1,2,3]

        elif rabbit[0] == size-1: #top row
            if rabbit[1] == 0: #right corner
                #obstacle below rabbit
                if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                    actions = [3]
                #obstacle to the left of rabbit
                elif stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                    actions = [0]
                else:
                    actions = [0,3]
            elif rabbit[1] == size-1: #left corner
                #obstacle below rabbit
                if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                    actions = [2]
                #obstacle to the right of rabbit
                elif stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                    actions = [0]
                else:
                    actions = [0,2]
            else:
                #obstacle below rabbit
                if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                    actions = [2,3]
                #obstacle to the right of rabbit
                elif stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                    actions = [0,3]
                #obstacle to the left of rabbit
                elif stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                    actions = [0,2]
                else:
                    actions = [0,2,3]

        #right side
        elif rabbit[1] == 0:
            #obstacle below rabbit
            if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                actions = [1,3]
            #obstacle above rabbit
            if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                actions = [0,3]
            #obstacle to the left of rabbit
            elif stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                actions = [0,1]

        #left side
        elif rabbit[1] == size-1:
            #obstacle below rabbit
            if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                actions = [1,2]
            #obstacle above rabbit
            if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                actions = [0,2]
            #obstacle to the right of rabbit
            elif stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                actions = [0,1]

        else:
            #obstacle below rabbit
            if stateMap[rabbit[0]-1][rabbit[1]] == 1 or stateMap[rabbit[0]-1][rabbit[1]] == 2:
                actions = [1,2,3]
            #obstacle above rabbit
            if stateMap[rabbit[0]+1][rabbit[1]] == 1 or stateMap[rabbit[0]+1][rabbit[1]] == 2:
                actions = [0,2,3]
            #obstacle to the right of rabbit
            if stateMap[rabbit[0]][rabbit[1]-1] == 1 or stateMap[rabbit[0]][rabbit[1]-1] == 2:
                actions = [0,1,3]
            #obstacle to the left of rabbit
            if stateMap[rabbit[0]][rabbit[1]+1] == 1 or stateMap[rabbit[0]][rabbit[1]+1] == 2:
                actions = [0,1,2]

        if stateMap[rabbit[0]][rabbit[1]] == 4: #is a berry bush
            actions = [4]

        return actions
            
    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        #r = 0
        #c = 0
        rabbit = state1["rabbit"]
        stateMap = state1["map"]
        size = state1["size"]
        #print("THis is the map:", state1.map)
        """
        for row in state1.map:
            c = 0
            for col in row:
                if (col == 6):
                    rabbit = (r, c, rabbit[2])
                c += 1
            r += 1
        """
        NewLoc = (rabbit[0], rabbit[1])
        Hunger = rabbit[2]
        if action == 0: #Move down
            if rabbit[0] != 0:
                if (((stateMap[rabbit[0]-1][rabbit[1]]) != 1) and
                    ((stateMap[rabbit[0]-1][rabbit[1]]) != 2)):
                    NewLoc = ((rabbit[0]-1), rabbit[1])
        if action == 1: #Move up
            if (rabbit[0] != (size-1)):
                if (((stateMap[rabbit[0]+1][rabbit[1]]) != 1) and 
                    ((stateMap[rabbit[0]+1][rabbit[1]]) != 2)): 
                    NewLoc = ((rabbit[0]+1), rabbit[1])
        if action == 2: #Move right
            if (rabbit[1] != (size-1)):
                if (((stateMap[rabbit[0]][rabbit[1]+1]) != 1) and 
                    ((stateMap[rabbit[0]][rabbit[1]+1]) != 2)):
                    NewLoc = (rabbit[0], (rabbit[1]+1))
        if action == 3: #Move left
            if (rabbit[1] != 0):
                if (((stateMap[rabbit[0]][rabbit[1]-1]) != 1) and
                    ((stateMap[rabbit[0]][rabbit[1]-1]) != 2)):
                    NewLoc = (rabbit[0], (rabbit[1]-1))
        if action == 4: #Eat Food
            if (stateMap[rabbit[0]][rabbit[1]] == 4):
                Hunger = 1
                stateMap[rabbit[0]][rabbit[1]] = 7

        """
        if ((NewLoc[0], NewLoc[1], Hunger) != rabbit):
            if state1.map[NewLoc[0]][NewLoc[1]] == 3:
                state1.map[NewLoc[0]][NewLoc[1]] = 3

            elif state1.map[NewLoc[0]][NewLoc[1]] == 4:
                if ate:
                    state1.map[NewLoc[0]][NewLoc[1]] = 7
                else:
                    state1.map[NewLoc[0]][NewLoc[1]] = 4

            elif state1.map[NewLoc[0]][NewLoc[1]] == 5:
                state1.map[NewLoc[0]][NewLoc[1]] = 5
            """

        #state1.rabbit = (NewLoc[0], NewLoc[1], Hunger)
        rabbit[0] = NewLoc[0]
        rabbit[1] = NewLoc[1]
        rabbit[2] = Hunger
        return state1

    def GOAL_TEST(state):
        #Rabbit is back in burrow and ate food
        rabbit = state["rabbit"]
        r = c = 0
        burrow = (-1,-1)
        stateMap = state["map"]
        for row in stateMap:
            c = 0
            for col in row:
                if col == 5:
                    burrow = (r, c)
                c += 1
            r+=1

        if ((rabbit[0], rabbit[1]) == burrow):
            if (rabbit[2] == 1):
                return True
        return False
        """
        if (state.rabbit[2] == 1):
            return True
        return False
        """

    def GOAL_TEST_FOOD(state):
        rabbit = state["rabbit"]
        if (rabbit[2] == 1):
            return True
        return False

    def STEP_COST(state, action, state1):
        stateMap = state["map"]
        rabbit = state1["rabbit"]
        #water cost 2
        if stateMap[rabbit[0]][rabbit[1]] == 3:
            cost = 5
        else:
            cost = 1
        return cost
    def HEURISTIC(state):
        foods = []
        r = c = 0
        stateMap = state["map"]
        rabbit = state["rabbit"]
        for row in stateMap:
            c = 0
            for col in row:
                if col == 4:
                    foods.append((r,c))
                c+=1
            r+=1

        h = math.inf
        for food in foods:
            row_dif = food[0] - rabbit[0]
            col_dif = food[1] - rabbit[1]
            new = abs(row_dif)+abs(col_dif)
            if new < h:
                h = new
        return h
    def HOMEHEURISTIC(state):
        r = c = 0
        burrow = (-1,-1)
        stateMap = state["map"]
        for row in stateMap:
            for col in row:
                if col == 5:
                    burrow = (r, c)
                c += 1
            r+=1
        h = math.inf
        rabbit = state["rabbit"]
        row_dif = burrow[0] - rabbit[0]
        col_dif = burrow[1] - rabbit[1]
        new = abs(row_dif)+abs(col_dif)
        if new < h:
            h = new
        return h
        

if __name__ == '__main__':
    state = RabbitForagingState()
    state.randomize()
    state = state.observation
    actions = RabbitForagingModel.ACTIONS(state)
    print(actions)

    print(state)
    state1 = RabbitForagingModel.RESULT(state, 0) #move down
    print(state1)

    state1 = RabbitForagingModel.RESULT(state, 1) #move up
    print(state1)

    state1 = RabbitForagingModel.RESULT(state, 2) #move right
    print(state1)

    state1 = RabbitForagingModel.RESULT(state, 3) #move right
    print(state1)

    state1 = RabbitForagingModel.RESULT(state, 4) #eat food
    print(state1)

    print(RabbitForagingModel.GOAL_TEST(state))
