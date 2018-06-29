import random
import math
from Utilities import Timer


class Animal:
    def __init__(self, width, height):
        # World Information
        self.worldWidth = width
        self.worldHeight = height

        # Animal Attributes
        # - GUI
        self.color = "#FFFFFF"
        self.size = 15
        # - Parameters
        self.hungerRate = 5
        self.maxAge = 30
        self.alertRange = 40
        self.hungerThreshold = 85
        self.desireRate = 20

        # Stauts
        # - Location
        self.x = random.randrange(0, width)
        self.y = random.randrange(0, height)
        self.v = random.randrange(30, 40)
        self.angle = random.randrange(0, 180) / math.pi
        # - Target
        self.tx = random.randrange(0, self.worldWidth)
        self.ty = random.randrange(0, self.worldHeight)
        # - Health
        self.dead = False
        self.food = 100
        self.age = 0
        self.desire = 50

        # Direction Control
        self.MoveToTarget()

    def Update(self, dt):
        """
        This Update method only implements the strolling behavior.
        """
        if (self.GetTargetDistance() < self.v):
            self.NewTarget()
            self.MoveToTarget()
        self.x += self.v * math.cos(self.angle) * dt
        self.y += self.v * math.sin(self.angle) * dt
        self.age += 1 * dt
        self.food -= 1 * dt
        self.desire += self.desireRate * dt

        if self.food <= 0 or self.age > self.maxAge: self.dead = True

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
        self.angle = math.atan2(y_dis, x_dis)
        '''
        self.dx = self.v * math.cos(angle)
        self.dy = self.v * math.sin(angle)
        '''

    def isHunger(self):
        return self.food < self.hungerThreshold

    def isDesireStrong(self):
        return self.desire > 80

class Sheep (Animal):
    def __init__(self, width, height):
        Animal.__init__(self, width, height)
        self.color = "#abe9ee"

        # Sheep Attributes:
        self.boostFactor = 1.5
        self.hungerFactor = self.boostFactor
        self.pregProbability = 0.75

        # Sheep Status
        self.danger = None

    def Update(self, dt):
        if self.danger == None:
            Animal.Update(self, dt)
        else:
            x_dis = self.danger.x - self.x
            y_dis = self.danger.y - self.y
            self.angle = math.atan2(-y_dis, x_dis)
            self.x += self.v * self.boostFactor * math.cos(self.angle) * dt
            self.y += self.v * self.boostFactor * math.sin(self.angle) * dt
            self.age += 1 * dt
            self.food -= self.hungerRate * dt * self.hungerFactor
            if self.CheckDangerDistance() > self.alertRange:
                self.danger = None

    def Mate(self, Sheep):
        if random.random() < self.pregProbability:
            Sheep.desire = 0
            self.desire = 0
            return Sheep(self.width, self.height)
        else:
            return None



    def Escape(self, wolf):
        # DEBUG Can replace wolf with wolfs
        self.danger = wolf

    def CheckDangerDistance(self):
        if self.danger == None:
            return None
        else:
            return math.sqrt((self.danger.x - self.x)**2 + (self.danger.y - self.y)**2)


class Wolf (Animal):
    def __init__(self, width, height):
        Animal.__init__(self, width, height)
        self.color = "#ec5d62"

        # Wolf Attributes:
        self.boostFactor = 2
        self.hungerFactor = self.boostFactor
        self.sheepFoodValue = 5
        self.pregProbability = 0.6

        # Wolf Status
        self.target = None

    def Update(self, dt):
        if self.target == None:
            Animal.Update(self, dt)
        else:
            x_dis = self.target.x - self.x
            y_dis = self.target.y - self.y
            self.angle = math.atan2(y_dis, x_dis)
            self.x += self.v * self.boostFactor * math.cos(self.angle) * dt
            self.y += self.v * self.boostFactor * math.sin(self.angle) * dt
            self.age += 1 * dt
            self.food -= self.hungerRate * dt * self.hungerFactor

    def Mate(self, wolf):
        if random.random() < self.pregProbability:
            wolf.desire = 0
            self.desire = 0
            return Wolf(self.width, self.height)
        else:
            return None


    def Chase(self, sheep):
        # DEBUG sheep can be replaced with sheeps, ask the wolf to choose which one to pick
        if self.isHunger():
            self.target = sheep
        else:
            print (self.food)

    def CheckSheepDistance(self):
        if self.target == None:
            return None
        else:
            return math.sqrt((self.target.x - self.x)**2 + (self.target.y - self.y)**2)

    def EatSheep(self, sheep = None):
        # DEBUG sheep here is just for debug
        if sheep == None:
            self.food += 10
            self.target.dead = True
            self.target = None

        else:
            self.food += self.sheepFoodValue
            sheep.dead = True
