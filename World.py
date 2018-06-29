from Entities import *
from Utilities import Timer, Point

INIT_SHEEPS_NUM = 50
INIT_WOLF_NUM = 20

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Game Attributes
        self.huntRange = 10

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
        for sheep in self.sheeps:
            sheep.Update(1 / self.fps)
            for wolf in self.wolfs:
                if sheep.danger == None and \
                self.DistanceBetween(sheep, wolf) < sheep.alertRange:
                    sheep.Escape(wolf)



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

        survivedSheeps = []
        survivedWolfs = []
        for sheep in self.sheeps:
            if not sheep.dead:
                survivedSheeps.append(sheep)

        for wolf in self.wolfs:
            if not wolf.dead:
                survivedWolfs.append(wolf)

        self.wolfs = survivedWolfs
        self.sheeps = survivedSheeps

    def Render(self, canvas):
        for sheep in self.sheeps:
            sheep.Render(canvas)

        for wolf in self.wolfs:
            wolf.Render(canvas)

    def DistanceBetween(self, a1, a2):
        return math.sqrt((a2.x - a1.x)**2 + (a2.y - a1.y)**2)
