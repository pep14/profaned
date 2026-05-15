import tkinter as tk
from elementary import *
from world import *
from keybinds import *

GRAVITY = -2
FRICTION = 0.8
DASH_COOLDOWN = 15
DASH_SPEED = 30
DASH_TIME = 8
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

        self.geometry("%ix%i" % WINDOW_DIMENSIONS.tuple)

        self.canvas = tk.Canvas(
            self,
            width=WINDOW_DIMENSIONS.x,
            height=WINDOW_DIMENSIONS.y,
            bg="black"
        )
        self.canvas.pack()

        self.focus_set()

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

        self.canvas.create_oval(
            screen_x - 50,
            screen_y - 200,
            screen_x + 50,
            screen_y + 0,
            fill="#FFFFFF"
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
