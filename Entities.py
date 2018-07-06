import random
import math
from Utilities import Timer

class Animal:
    def __init__(self, width, height, x = None, y = None, food = None):
        # World Information
        self.worldWidth = width
        self.worldHeight = height

        # Animal Attributes
        self.size = 10
        # - Parameters
        self.hungerRate = 10
        self.maxFood = 100
        self.hungerThreshold = 80
        self.boostFactor = random.randrange(10, 12) / 10.0
        self.hungerFactor = self.boostFactor ** (1/1.5)
        self.pregProbability = 0.75
        self.maxAge = 40
        self.matureAge = 3
        self.alertRange = 40
        self.desireThreshold = 30
        self.maxDesire = 100
        self.desireRate = 50


        # Stauts
        # - Location
        self.x = x if x != None else random.randrange(0, width)
        self.y = y if y != None else random.randrange(0, height)
        self.v = random.randrange(35, 45)
        self.angle = random.randrange(0, 180) / math.pi
        # - Target
        self.tx = random.randrange(0, self.worldWidth)
        self.ty = random.randrange(0, self.worldHeight)
        self.mateTarget = None
        # - Status
        self.dead = False
        self.isMature = False
        self.food = 85 if food == None else food
        # print("Food => {}".format(self.food))
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

    def RunToward(self, target, dt, reverse = False):
        x_dis = target.x - self.x
        y_dis = target.y - self.y
        self.angle = math.atan2(y_dis, x_dis)
        self.angle = self.angle + math.pi if reverse else self.angle
        self.x += self.v * self.boostFactor * math.cos(self.angle) * dt
        self.y += self.v * self.boostFactor * math.sin(self.angle) * dt

    def Mate(self, target):
        target.desire = 0
        target.mateTarget = None
        self.desire = 0
        self.mateTarget = None
        self.food - 5

    def isHunger(self):
        return self.food < self.hungerThreshold

    def isDesireStrong(self):
        return self.desire > self.desireThreshold


class Sheep (Animal):
    def __init__(self, width, height, x = None, y = None, food = None):
        Animal.__init__(self, width, height, x, y, food)

        # Sheep Attributes
        self.hungerRate = 30
        self.lowFoodThreshold = 50
        self.foodValue = random.randrange(25, 30)

        # Sheep Status
        self.danger = None

    def Update(self, dt):
        Animal.Update(self, dt)
        # Non danger status
        if self.danger == None:
            if self.mateTarget == None or self.food < self.lowFoodThreshold:
                # No mate target
                if (self.GetTargetDistance() < self.v):
                    self.NewTarget()
                self.MoveToTarget()
                self.x += self.v * math.cos(self.angle) * dt
                self.y += self.v * math.sin(self.angle) * dt
                # print("Food Drop => {}".format(self.hungerRate * dt)) # DEBUG
                self.food -= self.hungerRate * dt
            else:
                # has mate target
                self.RunToward(self.mateTarget, dt)
                self.food -= self.hungerRate * dt * self.hungerFactor
                if self.CheckDistanceTo(self.mateTarget) > self.alertRange:
                    self.mateTarget = None

        # In danger status
        else:
            self.RunToward(self.danger, dt, reverse = True)
            self.food -= self.hungerRate * dt * self.hungerFactor
            if self.CheckDistanceTo(self.danger) > self.alertRange:
                self.NewTarget()
                self.danger = None
        #
        # Check death
        if self.food <= 0 or self.age > self.maxAge: self.dead = True

    def EatGrass(self, dt, sheepNum):
        # print("sheepNum => {}".format(sheepNum))
        sheepNum = sheepNum - 5 if sheepNum - 5 > 0 else 0
         #print("Food Gain => {}".format(10 * dt * math.exp(- sheepNum))) # DEBUG
        self.food += self.hungerRate * 2.71 ** (- sheepNum) * dt * 1.1
        self.food = self.maxFood if self.food > self.maxFood else self.food

    def Mate(self, s):
        Animal.Mate(self, s)
        if random.random() < self.pregProbability:
            return Sheep(
                self.worldWidth, self.worldHeight,
                self.x, self.y,
                (s.food + self.food) / 2)
        else:
            return None

    def Escape(self, wolf):
        # DEBUG Can replace wolf with wolfs
        self.danger = wolf

class Wolf (Animal):
    def __init__(self, width, height, x = None, y = None):
        Animal.__init__(self, width, height, x, y)
        # Wolf Status
        self.maxAge *= 1.5
        self.pregProbability = 0.9
        self.boostFactor = random.randrange(17, 20) / 10.0
        self.hungerRate = 15
        self.huntRange = 20
        self.alertRange = 60
        self.lowFoodThreshold = 50
        self.desireRate = 30
        self.target = None

    def Update(self, dt):
        Animal.Update(self, dt)
        if self.target == None:
            if self.mateTarget == None or self.food < self.lowFoodThreshold:
                if (self.GetTargetDistance() < self.v):
                    self.NewTarget()
                self.MoveToTarget()
                self.x += self.v * math.cos(self.angle) * dt
                self.y += self.v * math.sin(self.angle) * dt
                self.food -= self.hungerRate * dt
            else:
                self.RunToward(self.mateTarget, dt)
                self.food -= self.hungerRate * dt * self.hungerFactor
                if self.CheckDistanceTo(self.mateTarget) > self.alertRange:
                    self.mateTarget = None
        else:
            self.RunToward(self.target, dt)
            self.food -= self.hungerRate * dt * self.hungerFactor
        if self.food <= 0 or self.age > self.maxAge: self.dead = True

    def Mate(self, w):
        Animal.Mate(self, w)
        if random.random() < self.pregProbability:
            # print("Wolf mate success")
            return Wolf(self.worldWidth, self.worldHeight, self.x, self.y)
        else:
            return None

    def Chase(self, sheep):
        # DEBUG sheep can be replaced with sheeps, ask the wolf to choose which one to pick
        if self.isHunger():
            self.target = sheep


    def CheckSheepDistance(self):
        if self.target == None:
            return None
        else:
            return math.sqrt((self.target.x - self.x)**2 + (self.target.y - self.y)**2)

    def EatSheep(self):
        self.food += self.target.foodValue
        self.target.dead = True
        self.target = None
