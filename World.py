from Entities import *
from Utilities import Timer, Point

INIT_SHEEPS_NUM = 40
INIT_WOLF_NUM = 7

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

        # Sheep alert
        for sheep in self.sheeps:
            sheep.Update(1 / self.fps)
            for wolf in self.wolfs:
                if sheep.danger == None and \
                self.DistanceBetween(sheep, wolf) < sheep.alertRange:
                    sheep.Escape(wolf)
        # Sheep mate
        newSheeps = []
        for i in range(len(self.sheeps)):
            for k in range(i+1, len(self.sheeps)):
                s1 = self.sheeps[i]
                s2 = self.sheeps[k]
                if s1.CheckDistanceTo(s2) < self.mateRange and s1.isDesireStrong() and s2.isMature:
                    sBaby = s1.Mate(s2)
                    if sBaby != None:
                        newSheeps.append(sBaby)
                        break


        # wolves alert
        for wolf in self.wolfs:
            wolf.Update(1 / self.fps) # Move the wolf
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
                w2 = self.wolfs[k]
                if w1.CheckDistanceTo(w2) < self.mateRange and w1.isDesireStrong():
                    wBaby = w1.Mate(w1)
                    if wBaby != None:
                        newWolves.append(wBaby)
                        break

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
