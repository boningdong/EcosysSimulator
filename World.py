from Entities import *
from Utilities import Timer, Point

INIT_SHEEPS_NUM = 20
INIT_WOLF_NUM = 30

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # fps management
        self.fps = 120
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
        self.timer.Tick()
        if self.timer.counter > 1 / self.fps:
            self.timer.Reset()
            for sheep in self.sheeps:
                sheep.Update()
                if self.CheckHunting(sheep):
                    sheep.dead = True

            for wolf in self.wolfs:
                wolf.Update()
            
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
    
    def CheckHunting(self, sheep):
        for wolf in self.wolfs:
            dis = math.sqrt((wolf.x - sheep.x)**2 + (wolf.y - sheep.y)**2)
            if dis < 20:
                wolf.EatSheep()
                return True
        return False
    
            
