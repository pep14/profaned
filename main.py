import tkinter as tk
from elementary import *
from world import *
from keybinds import *

GRAVITY = -2
FRICTION = 0.8
DASH_COOLDOWN = 15
DASH_SPEED = 28
DASH_TIME = 14
JUMP_STRENGTH = 25
PLR_SPEED = 3

KB = Keybinds(
    move_left="a",
    move_right="d",
    jump="space",
    dash="Shift_L"
)

WINDOW_DIMENSIONS = Dim2(1280, 720)
WORLD = World()
PLAYER = Player(0, 0, GRAVITY, FRICTION)


class Profaned(tk.Tk):
    def __init__(self):
        super().__init__()

        # window
        self.geometry("%ix%i" % WINDOW_DIMENSIONS.tuple)

        self.canvas = tk.Canvas(
            self,
            width=WINDOW_DIMENSIONS.x,
            height=WINDOW_DIMENSIONS.y,
            bg="black"
        )
        self.canvas.pack()

        self.focus_set()

        # textures
        self.textures = {
            "johnR": tk.PhotoImage(file='./textures/john-profaned-sword-R.png'),
            "johnL": tk.PhotoImage(file='./textures/john-profaned-sword-L.png'),
            "johnSlideR": tk.PhotoImage(file='./textures/john-slide-R.png'),
            "johnSlideL": tk.PhotoImage(file='./textures/john-slide-L.png'),
            "johnJumpR": tk.PhotoImage(file='./textures/john-jumping-R.png'),
            "johnJumpL": tk.PhotoImage(file='./textures/john-jumping-L.png'),
        }

        # inputs
        self.keysDown = set()

        self.bind("<KeyPress>", self._keyPressed)
        self.bind("<KeyRelease>", self._keyReleased)

    def run(self):
        if KB.jump in self.keysDown and PLAYER.grounded:
            PLAYER.vy = JUMP_STRENGTH

        if not PLAYER.dashing:
            if KB.move_left in self.keysDown:
                PLAYER.vx -= PLR_SPEED
                PLAYER.facing = -1

            if KB.move_right in self.keysDown:
                PLAYER.vx += PLR_SPEED
                PLAYER.facing = 1

        if PLAYER.dashCD > 0:
            PLAYER.dashCD -= 1

        if KB.dash in self.keysDown and PLAYER.dashCD == 0 and not PLAYER.dashing:
            PLAYER.dashing = True
            PLAYER.dash_time = DASH_TIME
            PLAYER.vx = PLAYER.facing * DASH_SPEED
            PLAYER.dashCD = DASH_COOLDOWN

        if PLAYER.dashing:
            PLAYER.vx = PLAYER.facing * DASH_SPEED

            PLAYER.dash_time -= 1

            if PLAYER.dash_time <= 0:
                PLAYER.dashing = False

        PLAYER.update()
        self.render()

        self.after(20, self.run)

    def render(self):
        self.canvas.delete("all")

        screen_x = PLAYER.x + WINDOW_DIMENSIONS.x // 2
        screen_y = WINDOW_DIMENSIONS.y - PLAYER.y

        self.canvas.create_rectangle(
            screen_x - 64,
            screen_y - 256,
            screen_x + 64,
            screen_y + 0,
            fill="#000000",
            outline="#ff0000"
        )

        if PLAYER.dashing:
            john = self.textures["johnSlideR"] if PLAYER.facing == 1 else self.textures["johnSlideL"]

            self.canvas.create_image(
                screen_x,
                screen_y - 64,
                image=john
            )
        elif PLAYER.grounded:
            john = self.textures["johnR"] if PLAYER.facing == 1 else self.textures["johnL"]

            self.canvas.create_image(
                screen_x,
                screen_y - 128,
                image=john
            )
        else:
            john = self.textures["johnJumpR"] if PLAYER.facing == 1 else self.textures["johnJumpL"]

            self.canvas.create_image(
                screen_x,
                screen_y - 128,
                image=john
            )

    def _keyPressed(self, event) -> None:
        if event.keysym in self.keysDown: return

        print(event.keysym)
        self.keysDown.add(event.keysym)

    def _keyReleased(self, event) -> None:
        print(event.keysym)
        self.keysDown.discard(event.keysym)

if __name__ == "__main__":
    game = Profaned()
    game.run()
    game.mainloop()
