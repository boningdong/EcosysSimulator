from Entities import *
from Utilities import Timer, Point

INIT_SHEEPS_NUM = 40
INIT_WOLF_NUM = 15

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

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
        self.timer.Tick() # Update game timer

        for s in self.sheeps:
            s.Update(1 / self.fps)
            self.Reposition(s)

        # Sheep alert
        for s in self.sheeps:
            for wolf in self.wolfs:
                if s.danger == None and \
                self.DistanceBetween(s, wolf) < s.alertRange:
                    s.Escape(wolf)
        # Sheep mate
        newSheeps = []
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

        for wolf in self.wolfs:
            wolf.Update(1 / self.fps) # Move the wolf

        # wolves alert
        for wolf in self.wolfs:

            for sheep in self.sheeps:
                # Locate a target for the wolf
                if wolf.target == None and \
                self.DistanceBetween(sheep, wolf) < wolf.alertRange and sheep.dead != True:
                    wolf.Chase(sheep)
                # If the target within the range, eat
                if wolf.CheckSheepDistance() != None and \
                wolf.CheckSheepDistance() < self.huntRange and sheep.dead != True:
                    wolf.EatSheep()

        # Wolves mate
        newWolves = []
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
