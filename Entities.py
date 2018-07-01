import random
import math
from Utilities import Timer


class Animal:
    def __init__(self, width, height, x = None, y = None):
        # World Information
        self.worldWidth = width
        self.worldHeight = height

        # Animal Attributes
        self.size = 15
        # - Parameters
        self.hungerRate = 1
        self.maxFood = 100
        self.hungerThreshold = 85
        self.maxAge = 100
        self.matureAge = 15
        self.alertRange = 40
        self.desireThreshold = 60
        self.maxDesire = 100
        self.desireRate = 40


        # Stauts
        # - Location
        self.x = x if x != None else random.randrange(0, width)
        self.y = y if y != None else random.randrange(0, height)
        self.v = random.randrange(30, 40)
        self.angle = random.randrange(0, 180) / math.pi
        # - Target
        self.tx = random.randrange(0, self.worldWidth)
        self.ty = random.randrange(0, self.worldHeight)
        # - Health
        self.dead = False
        self.isMature = False
        self.food = 100
        self.age = 0
        self.desire = 0

        # Direction Control
        self.MoveToTarget()

    def Update(self, dt):
        """
        This Update method only implements the strolling behavior.
        """
        """
        if (self.GetTargetDistance() < self.v):
            self.NewTarget()
        self.MoveToTarget()
        self.x += self.v * math.cos(self.angle) * dt
        self.y += self.v * math.sin(self.angle) * dt
        """
        self.age += 1 * dt
        if not self.isMature and self.age > self.matureAge:
            self.isMature = True
        self.desire += self.desireRate * dt if self.isMature else 0

    def NewTarget(self):
        self.tx = random.randrange(0, self.worldWidth)
        self.ty = random.randrange(0, self.worldHeight)

    def GetTargetDistance(self):
        d = math.sqrt((self.tx - self.x)**2 + (self.ty - self.y)**2)
        return d

    def CheckDistanceTo(self, obj):
        return math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)

    def MoveToTarget(self):
        x_dis = self.tx - self.x
        y_dis = self.ty - self.y
        self.angle = math.atan2(y_dis, x_dis)

    def isHunger(self):
        return self.food < self.hungerThreshold

    def isDesireStrong(self):
        return self.desire > self.desireThreshold

class Sheep (Animal):
    def __init__(self, width, height, x = None, y = None):
        Animal.__init__(self, width, height, x, y)

        # Sheep Attributes:
        self.boostFactor = 1.5
        self.hungerFactor = self.boostFactor
        self.pregProbability = 0.7

        # Sheep Status
        self.danger = None

    def Update(self, dt):
        Animal.Update(self, dt)
        if self.danger == None:
            if (self.GetTargetDistance() < self.v):
                self.NewTarget()
            self.MoveToTarget()
            self.x += self.v * math.cos(self.angle) * dt
            self.y += self.v * math.sin(self.angle) * dt
            self.food -= self.hungerRate * dt
        else:
            x_dis = self.danger.x - self.x
            y_dis = self.danger.y - self.y
            self.angle = math.atan2(y_dis, x_dis) + math.pi
            self.x += self.v * self.boostFactor * math.cos(self.angle) * dt
            self.y += self.v * self.boostFactor * math.sin(self.angle) * dt
            self.age += 1 * dt
            self.food -= self.hungerRate * dt * self.hungerFactor
            if self.CheckDangerDistance() > self.alertRange:
                self.danger = None
        if self.food <= 0 or self.age > self.maxAge: self.dead = True

    def Mate(self, s):
        s.desire = 0
        self.desire = 0
        if random.random() < self.pregProbability:
            return Sheep(self.worldWidth, self.worldHeight, self.x, self.y)
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
    def __init__(self, width, height, x = None, y = None):
        Animal.__init__(self, width, height, x, y)

        # Wolf Attributes:
        self.boostFactor = 2
        self.hungerFactor = self.boostFactor
        self.sheepFoodValue = 5
        self.pregProbability = 0.6

        # Wolf Status
        self.target = None

    def Update(self, dt):
        Animal.Update(self, dt)
        if self.target == None:
            if (self.GetTargetDistance() < self.v):
                self.NewTarget()
            self.MoveToTarget()
            self.x += self.v * math.cos(self.angle) * dt
            self.y += self.v * math.sin(self.angle) * dt
            self.food -= self.hungerRate * dt
        else:
            x_dis = self.target.x - self.x
            y_dis = self.target.y - self.y
            self.angle = math.atan2(y_dis, x_dis)
            self.x += self.v * self.boostFactor * math.cos(self.angle) * dt
            self.y += self.v * self.boostFactor * math.sin(self.angle) * dt
            self.age += 1 * dt
            self.food -= self.hungerRate * dt * self.hungerFactor
        if self.food <= 0 or self.age > self.maxAge: self.dead = True

    def Mate(self, w):
        w.desire = 0
        self.desire = 0
        if random.random() < self.pregProbability:
            print("Wolf mate success")
            return Wolf(self.worldWidth, self.worldHeight, self.x, self.y)
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

    def EatSheep(self):
        self.food += 10
        self.target.dead = True
        self.target = None
