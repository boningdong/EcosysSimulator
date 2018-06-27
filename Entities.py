import random
import math
from Utilities import Timer


class Animal:
    LIFE_TIME = 20 # in seconds
    def __init__(self, width, height):
        # World Information
        self.worldWidth = width
        self.worldHeight = height
        self.lifeTimer = Timer()

        # Animal Status
        self.x = random.randrange(0, width)
        self.y = random.randrange(0, height)
        self.color = "#FFFFFF"
        self.v = random.randrange(1, 5)
        self.size = 15
        
        # Stauts
        self.dead = False
        self.food = 100

        # Direction Control
        self.NewTarget()
        self.MoveToTarget()
    
    def Update(self):
        self.lifeTimer.Tick()
        if (self.GetTargetDistance() < self.v):
            self.NewTarget()
            self.MoveToTarget()
        self.x += self.dx
        self.y += self.dy
        if self.food <= 0 or self.lifeTimer.TotalTime() >= Animal.LIFE_TIME: self.dead = True

    def Render(self, canvas):
        canvas.create_rectangle(self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2, fill=self.color)
    
    def NewTarget(self):
        self.tx = random.randrange(0, self.worldWidth)
        self.ty = random.randrange(0, self.worldHeight)

    def GetTargetDistance(self):
        d = math.sqrt((self.tx - self.x)**2 + (self.ty - self.y)**2)
        return d

    def MoveToTarget(self):
        x_dis = self.tx - self.x
        y_dis = self.ty - self.y
        angle = math.atan2(y_dis, x_dis)
        self.dx = self.v * math.cos(angle)
        self.dy = self.v * math.sin(angle)




class Sheep (Animal):
    def __init__(self, width, height):
        Animal.__init__(self, width, height)
        self.color = "#abe9ee"
    
    def Update(self):
        Animal.Update(self)
        self.lifeTimer.Reset()

class Wolf (Animal):
    HUNGER_RATE = 20
    def __init__(self, width, height):
        Animal.__init__(self, width, height)
        self.color = "#ec5d62"
    
    def Update(self):
        Animal.Update(self)
        self.food -= self.lifeTimer.counter * Wolf.HUNGER_RATE
        # DEBUG
        # print ("DEBUG: Worlf Food = {}".format(self.food))
        self.lifeTimer.Reset()
    
    def EatSheep(self):
        self.food += 10