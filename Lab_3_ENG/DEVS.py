# -*- coding: cp1251 -*-

# Queue of Events
class EventsQueue:
    def __init__(self):
        self.globalTime = 0
        self.MEvents = []
              
    def QueueSize(self):
        return len(self.MEvents)

    def AddEvent(self,MEvent):        
        count =  len(self.MEvents)
        if count == 0:            
            self.MEvents.append(MEvent)
            return 0            

        if(MEvent.eTime >= self.MEvents[count - 1].eTime ):            
            self.MEvents.append(MEvent)
            return 0                                     
        # Place event to the middle of the queue
        for i in range(0,count-1):
            if (MEvent.eTime >= self.MEvents[i].eTime):
                if (MEvent.eTime < self.MEvents[i + 1].eTime):
                    self.MEvents.insert(i + 1, MEvent)
                    return 0

    def ProcessNextEvent(self):                    
        if (len(self.MEvents) == 0):
            return 0
        self.MEvents[0].Execute()
        self.globalTime = self.MEvents[0].eTime        
        del self.MEvents[0]

    def Clear(self):
        self.globalTime = 0
        self.MEvents = []

class Server:
    # simulation attributes
    Active = True
    serverIdle = True
    lastServedTime = 0 # for Idle time

# Discrete Event System Specification
class DEVS:
    EQ = EventsQueue()

    singleQueue = False
    dynamicQueues = False

    stats = []
    newId = 0
    GlobalTime = 0.0
    NumServers = 5
    customerQueues = [None] * NumServers
    ServerNumStats = [(0.0, NumServers - 1)]

    def __init__(self):
        pass

    @staticmethod    
    def ProcessNextEvent():        
        DEVS.EQ.ProcessNextEvent()
        DEVS.GlobalTime = DEVS.EQ.globalTime

    @staticmethod   
    def GetShortestQueue():
        min_queue_len = 10000 # BUG
        queue_idx = 0

        for idx, queue in enumerate(DEVS.customerQueues):
            if len(queue) < min_queue_len and DEVS.Servers[idx].Active:
                queue_idx = idx
                min_queue_len = len(queue)

        return queue_idx

    @staticmethod   
    def GetFreeServer():
        for idx,server in enumerate(DEVS.Servers):
            if server.serverIdle and server.Active:
                return idx
        return -1


    @staticmethod    
    def Clear():        
        DEVS.EQ.Clear()
        DEVS.GlobalTime = 0.0
        DEVS.newId = 0
        DEVS.stats = []
        DEVS.customerQueues = [None] * DEVS.NumServers
        DEVS.ServerNumStats = [(0.0, DEVS.NumServers - 1)]