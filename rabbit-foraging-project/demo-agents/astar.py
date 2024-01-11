import queue
import rabbit_foraging

class Node:
    def __init__(self, f, state, pnode, action, depth, g):
        self.state = state
        self.pnode = pnode
        self.action = action
        self.depth = depth
        self.f = f
        self.g = g

    def getDepth(self):
        return self.depth
    def getAction(self):
        return self.action
    def getPnode(self):
        return self.pnode
    def getState(self):
        return self.state
    def getG(self):
        return self.g
    def getF(self):
        return self.f

    def __lt__(self, other):
        return self.f < other.f

def astar_search(s0):
    reached = {}
    q = queue.PriorityQueue()
    q.put(s0)
    reached[tuple(s0.getState()["rabbit"])] = s0
    while not q.empty():
        #print("Before", q.queue)
        s = q.get()
        #print("After", q.queue)
        if rabbit_foraging.RabbitForagingModel.GOAL_TEST_FOOD(s.getState()):
            return s
        for a in rabbit_foraging.RabbitForagingModel.ACTIONS(s.getState()):
            r = rabbit_foraging.RabbitForagingModel.RESULT(s.getState(), a)
            #print("new rabbit:", r.rabbit)
            g = rabbit_foraging.RabbitForagingModel.STEP_COST(s.getState(), a, r) + s.getG()
            h = rabbit_foraging.RabbitForagingModel.HEURISTIC(s.getState())
            #print("r", r.rabbit)
            #print("reached", reached)
            #print(g, "<", reached[s.getState().rabbit].getG())
            if (not (tuple(r["rabbit"])) in reached) or (g < reached[tuple(s.getState()["rabbit"])].getG()):
                #print("good rabbit", r.rabbit)
                s1 = Node(g+h, r, s, a, s.getDepth()+1, g)
                q.put(s1)
                reached[tuple(r["rabbit"])] = s1
    return False

def astar_search_home(s0):
    reached = {}
    q = queue.PriorityQueue()
    q.put(s0)
    reached[tuple(s0.getState()["rabbit"])] = s0
    while not q.empty():
        s = q.get()
        if rabbit_foraging.RabbitForagingModel.GOAL_TEST(s.getState()):
            return s
        for a in rabbit_foraging.RabbitForagingModel.ACTIONS(s.getState()):
            r = rabbit_foraging.RabbitForagingModel.RESULT(s.getState(), a)
            g = rabbit_foraging.RabbitForagingModel.STEP_COST(s.getState(), a, r) + s.getG()
            h = rabbit_foraging.RabbitForagingModel.HOMEHEURISTIC(s.getState())
            if (not (tuple(r["rabbit"])) in reached) or (g < reached[tuple(s.getState()["rabbit"])].getG()):
                s1 = Node(g+h, r, s, a, s.getDepth()+1, g)
                q.put(s1)
                reached[tuple(r["rabbit"])] = s1
    return False
