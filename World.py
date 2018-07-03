from Entities import *
from Utilities import Timer, Point

INIT_SHEEPS_NUM = 50
INIT_WOLF_NUM = 10

MAP_X_BLOCK = 40
MAP_Y_BLOCK = 30

def SetInRange(x0, x1, val):
    if x0 <= val < x1:
        return val
    else:
        if val < x0:
            return 0
        else:
            return x1 - 1

class MapManager:
    def __init__(self, width, height):
        self.map_width = width
        self.map_height = height
        self.xBlocks = width / MAP_X_BLOCK
        self.yBlocks = height / MAP_Y_BLOCK
        self.map = []
        self.Reset()

    def Reset(self):
        self.map = []
        for x in range(MAP_X_BLOCK):
            self.map.append([])
            for y in range(MAP_Y_BLOCK):
                self.map[-1].append({'Sheeps':[], 'Wolfs':[]})

    def SaveObject(self, obj):
        (x, y) = self.Hash(obj)
        if isinstance(obj, Sheep):
            self.map[x][y]['Sheeps'].append(obj)
        elif isinstance(obj, Wolf):
            self.map[x][y]['Wolfs'].append(obj)
        else:
            print("Invalid input type. Game object must be a animal.")

    def GetObjectsInRanger(self, x, y, r):
        xx0 = (x - r) if x >= r else 0
        xx1 = (x + r) if (x + r) < self.map_width else self.map_width - 1
        yy0 = (y - r) if y >= r else 0
        yy1 = (y + r) if (y + r) < self.map_height else self.map_height - 1

        x0, x1 = int(xx0 // self.xBlocks), int(xx1 // self.xBlocks)
        y0, y1 = int(yy0 // self.yBlocks), int(yy1 // self.yBlocks)

        results = {'Sheeps': [], 'Wolfs': []}
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                results['Sheeps'] += self.map[x][y]['Sheeps']
                results['Wolfs'] += self.map[x][y]['Wolfs']

        return results

    def GetObjects(self, x, y):
        """
        Return type:
        {'Sheeps': [sheep list], 'Wolfs': [Wolves list]}
        """
        return self.map[x][y]

    def Hash(self, obj):
        xx, yy = SetInRange(0, self.map_width, obj.x), SetInRange(0, self.map_height, obj.y)
        x = int (xx // self.xBlocks)
        y = int (yy // self.yBlocks)
        return (x, y)

    def Log(self):
        msg = ""
        for y in range(MAP_Y_BLOCK):
            for x in range(MAP_X_BLOCK):
                objs = self.map[x][y]
                msg += "[s:{}, w:{}]".format(len(objs['Sheeps']), len(objs['Wolfs']))
            msg += "\n"
        msg += "\n"
        print (msg)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mapManager = MapManager(width, height)

        # Game Attributes
        self.huntRange = 10
        self.mateRange = 10

        # fps management
        self.fps = 30
        self.timer = Timer()

        # Game Entites:
        self.wolfs = []
        self.sheeps = []

    def StartGame(self):
        for i in range(INIT_SHEEPS_NUM):
            self.sheeps.append(Sheep(self.width, self.height))
        for i in range(INIT_WOLF_NUM):
            self.wolfs.append(Wolf(self.width, self.height))

    def Update(self):
        # self.timer.Tick() # Update game timer

        self.mapManager.Reset()

        for s in self.sheeps:
            s.Update(1 / self.fps)
            self.Reposition(s)
            self.mapManager.SaveObject(s)

        for w in self.wolfs:
            w.Update(1 / self.fps) # Move the wolves
            self.mapManager.SaveObject(w)

        # Sheep alert
        for s in self.sheeps:
            #for wolf in self.wolfs:
            for wolf in self.mapManager.GetObjectsInRanger(s.x, s.y, s.alertRange)['Wolfs']:
                if s.danger == None and \
                self.DistanceBetween(s, wolf) < s.alertRange:
                    s.Escape(wolf)

        # Sheep mate
        newSheeps = []
        """
        for i in range(len(self.sheeps)):
            for k in range(i+1, len(self.sheeps)):
                s1 = self.sheeps[i]
                if not s1.isDesireStrong():
                    s1.mateTarget = None
                    break
                # if it already has a target in range, then stick with the target.
                if s1.mateTarget != None:
                    if s1.CheckDistanceTo(s1.mateTarget) < self.mateRange:
                        ss = s1.Mate(s1.mateTarget)
                        if ss != None:
                            newSheeps.append(ss)
                    break
                # if it has no target, then locate a new target.
                s2 = self.sheeps[k]
                if s1.CheckDistanceTo(s2) < s1.alertRange and s2.isMature:
                    print ("[Sheep] => Located mate target!") # DEBUG
                    s1.mateTarget = s2
        """
        for s1 in self.sheeps:
            for s2 in self.mapManager.GetObjectsInRanger(s1.x, s1.y, s1.alertRange)['Sheeps']:
                if not s1.isDesireStrong():
                    s1.mateTarget = None
                    break
                # if it already has a target in range, then stick with the target.
                if s1.mateTarget != None:
                    if s1.CheckDistanceTo(s1.mateTarget) < self.mateRange:
                        ss = s1.Mate(s1.mateTarget)
                        if ss != None:
                            newSheeps.append(ss)
                    break
                # if it has no target, then locate a new target.
                if s1.CheckDistanceTo(s2) < s1.alertRange and s2.isMature:
                    # print ("[Sheep] => Located mate target!") # DEBUG
                    s1.mateTarget = s2


        # wolves alert
        for wolf in self.wolfs:
            for sheep in self.mapManager.GetObjectsInRanger(wolf.x, wolf.y, wolf.alertRange)['Sheeps']:
            #for sheep in self.sheeps:
                # Locate a target for the wolf
                if wolf.target == None and \
                self.DistanceBetween(sheep, wolf) < wolf.alertRange and not sheep.dead:
                    wolf.Chase(sheep)
                # If the target within the range, eat
                if wolf.CheckSheepDistance() != None and \
                wolf.CheckSheepDistance() < self.huntRange and sheep.dead != True:
                    wolf.EatSheep()

        # Wolves mate
        newWolves = []
        """
        for i in range(len(self.wolfs)):
            for k in range(i+1, len(self.wolfs)):
                w1 = self.wolfs[i]
                if not w1.isDesireStrong():
                    break
                #  if it already has a target in range, then stick with the target.
                if w1.mateTarget != None:
                    if w1.CheckDistanceTo(w1.mateTarget) < self.mateRange and w1.isDesireStrong():
                        ww  = w1.Mate(w1.mateTarget)
                        if ww != None:
                            newWolves.append(ww)
                # if it has no mate target, then locate a new target.
                w2 = self.wolfs[k]
                if w1.CheckDistanceTo(w2) < w1.alertRange and w2.isMature:
                    print ("[Wolf] => Located mate target!") # DEBUG
                    w1.mateTarget = w2
        """
        for w1 in self.wolfs:
            for w2 in self.mapManager.GetObjectsInRanger(w1.x, w1.y, w1.alertRange)['Wolfs']:
                if not w1.isDesireStrong():
                    w1.mateTarget = None
                    break
                #  if it already has a target in range, then stick with the target.
                if w1.mateTarget != None:
                    if w1.CheckDistanceTo(w1.mateTarget) < self.mateRange and w1.isDesireStrong():
                        ww  = w1.Mate(w1.mateTarget)
                        if ww != None:
                            newWolves.append(ww)
                # if it has no mate target, then locate a new target.
                if w1.CheckDistanceTo(w2) < w1.alertRange and w2.isMature:
                    print ("[Wolf] => Located mate target!") # DEBUG
                    w1.mateTarget = w2

        survivedSheeps = []
        survivedWolfs = []
        for sheep in self.sheeps:
            if not sheep.dead:
                survivedSheeps.append(sheep)

        for wolf in self.wolfs:
            if not wolf.dead:
                survivedWolfs.append(wolf)

        self.wolfs = survivedWolfs + newWolves
        self.sheeps = survivedSheeps + newSheeps

    def DistanceBetween(self, a1, a2):
        return math.sqrt((a2.x - a1.x)**2 + (a2.y - a1.y)**2)

    def Reposition(self, obj):
        if obj.x > self.width or obj.x < 0 or obj.y > self.height or obj.y < 0:
            obj.x = obj.x % self.width if obj.x > self.width or obj.x < -1 else obj.x
            obj.y = obj.y % self.height if obj.y > self.height or obj.y < -1 else obj.y
            obj.NewTarget()
