from World import World
import tkinter

GAME_WIDTH = 800
GAME_HEIGHT = 600

SHEEP_COLOR = "#abe9ee"
WOLF_COLOR = "#ec5d62"

FOOD_BAR_COLOR = "#33cc33"
DESIRE_BAR_COLOR = "#cc00cc"
LIFE_BAR_COLOR = "#ff0000"

class Frame:
    def __init__(self):
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.frame = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.frame, width = self.width, height = self.height)

        # Game World
        self.world = World(self.width, self.height)
        # Pack
        self.canvas.pack()

    def RunGame(self):
        self.world.StartGame()
        self.frame.mainloop()

    def GameLoop(self):
        self.Update()
        self.Render()
        self.frame.after(10, self.GameLoop)

    def Update(self):
        self.world.Update()

    # Render Part
    def Render(self):
        self.canvas.delete("all")
        # self.world.Render(self.canvas)
        # pass
        for sheep in self.world.sheeps:
            self.canvas.create_rectangle(
                sheep.x - sheep.size / 2,
                sheep.y - sheep.size / 2,
                sheep.x + sheep.size / 2,
                sheep.y + sheep.size / 2,
                fill=SHEEP_COLOR
            )
            self.ShowStatus(sheep)
        for wolf in self.world.wolfs:
            self.canvas.create_rectangle(
                wolf.x - wolf.size / 2,
                wolf.y - wolf.size / 2,
                wolf.x + wolf.size / 2,
                wolf.y + wolf.size / 2,
                fill=WOLF_COLOR
            )
            self.ShowStatus(wolf)

    def ShowStatus(self, animal):
        BAR_H = 2
        BAR_GAP = 1
        h_offset = animal.size / 2 + (BAR_H + BAR_GAP)* 3
        l = animal.size * 1.5
        y = animal.y - h_offset
        x = animal.x

        # Life bar
        life_percent = (animal.maxAge - animal.age) / animal.maxAge
        self.canvas.create_rectangle(
            x - l/2,
            y - BAR_H/2,
            x - l/2 + l * life_percent,
            y + BAR_H/2,
            outline = '',
            fill=LIFE_BAR_COLOR
        )

        # Food bar
        food_percent = animal.food / animal.maxFood
        food_percent = 1 if food_percent > 1 else food_percent
        self.canvas.create_rectangle(
            x - l/2,
            y + BAR_H + BAR_GAP - BAR_H/2,
            x - l/2 + l * food_percent,
            y + BAR_H + BAR_GAP + BAR_H/2,
            outline = '',
            fill=FOOD_BAR_COLOR
        )

        # Desire bar
        desire_percent = animal.desire / animal.maxDesire
        desire_percent = 1 if desire_percent > 1 else desire_percent
        self.canvas.create_rectangle(
            x - l/2,
            y + (BAR_H + BAR_GAP)*2 - BAR_H/2,
            x - l/2 + l * desire_percent,
            y + (BAR_H + BAR_GAP)*2 + BAR_H/2,
            outline = '',
            fill=DESIRE_BAR_COLOR
        )


if __name__ == "__main__":
    frame = Frame()
    frame.GameLoop()
    frame.RunGame()
