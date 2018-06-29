from World import World
import tkinter

GAME_WIDTH = 1024
GAME_HEIGHT = 768

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

    def Render(self):
        self.canvas.delete("all")
        self.world.Render(self.canvas)
        pass

if __name__ == "__main__":
    frame = Frame()
    frame.GameLoop()
    frame.RunGame()
