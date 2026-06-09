import tkinter as tk
from entities import *
from world import *
from keybinds import *

DEBUG = True

GRAVITY = -2
FRICTION = 0.8
DASH_COOLDOWN = 15
DASH_SPEED = 28
DASH_TIME = 14
JUMP_STRENGTH = 25
PLR_SPEED = 3
ATTACK_TIME = 10
ATTACK_COOLDOWN = 15

KB = Keybinds(
    move_left="a",
    move_right="d",
    jump="space",
    dash="Shift_L",
    attack="k"
)

WINDOW_DIMENSIONS = Vector2(1280, 720)
WORLD = World()
PLAYER = Player(0, 0, GRAVITY, FRICTION, WINDOW_DIMENSIONS)


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
            "johnAttackR": tk.PhotoImage(file='./textures/john-attack-R.png'),
            "johnAttackL": tk.PhotoImage(file='./textures/john-attack-L.png'),
        }

        # inputs
        self.keysDown = set()

        self.bind("<KeyPress>", self._keyPressed)
        self.bind("<KeyRelease>", self._keyReleased)

    def run(self):
        if KB.jump in self.keysDown and PLAYER.grounded:
            PLAYER.vy = JUMP_STRENGTH

        if not (PLAYER.attacking or PLAYER.dashing):
            if KB.move_left in self.keysDown:
                PLAYER.vx -= PLR_SPEED
                PLAYER.facing = -1

            if KB.move_right in self.keysDown:
                PLAYER.vx += PLR_SPEED
                PLAYER.facing = 1

        if PLAYER.dashCD > 0:
            PLAYER.dashCD -= 1

        if KB.dash in self.keysDown and PLAYER.dashCD == 0 and not (PLAYER.dashing or PLAYER.attacking):
            PLAYER.dashing = True
            PLAYER.dashT = DASH_TIME
            PLAYER.vx = PLAYER.facing * DASH_SPEED
            PLAYER.dashCD = DASH_COOLDOWN

        if PLAYER.dashing:
            PLAYER.vx = PLAYER.facing * DASH_SPEED

            PLAYER.dashT -= 1

            if PLAYER.dashT <= 0:
                PLAYER.dashing = False

        if PLAYER.attackCD > 0:
            PLAYER.attackCD -= 1

        if KB.attack in self.keysDown and PLAYER.attackCD == 0 and not (PLAYER.dashing or PLAYER.attacking):
            PLAYER.attacking = True
            PLAYER.attackT = ATTACK_TIME
            PLAYER.attackCD = ATTACK_COOLDOWN

        if PLAYER.attacking:
            PLAYER.attackT -= 1

            if PLAYER.attackT <= 0:
                PLAYER.attacking = False

        PLAYER.update()
        self.render()

        self.after(20, self.run)

    def render(self):
        self.canvas.delete("all")

        hitbox = PLAYER.hitbox
        hurtbox = PLAYER.hurtbox

        if DEBUG:
            if not PLAYER.dashing:
                self.canvas.create_rectangle(
                    hurtbox[0].x,
                    hurtbox[0].y,
                    hurtbox[1].x,
                    hurtbox[1].y,
                    outline="#ff0000"
                )
            if PLAYER.attacking:
                self.canvas.create_rectangle(
                    hitbox[0].x,
                    hitbox[0].y,
                    hitbox[1].x,
                    hitbox[1].y,
                    outline="#ffff00"
                )

        if PLAYER.attacking:
            if PLAYER.facing == 1:
                self.canvas.create_image(
                    hurtbox[0].x + 98,
                    hurtbox[0].y + 128,
                    image=self.textures["johnAttackR"]
                )
            else:
                self.canvas.create_image(
                    hurtbox[0].x + 30,
                    hurtbox[0].y + 128,
                    image=self.textures["johnAttackL"]
                )
        elif PLAYER.dashing:
            john = self.textures["johnSlideR"] if PLAYER.facing == 1 else self.textures["johnSlideL"]

            self.canvas.create_image(
                hurtbox[0].x + 64,
                hurtbox[0].y + 192,
                image=john
            )
        elif PLAYER.grounded:
            john = self.textures["johnR"] if PLAYER.facing == 1 else self.textures["johnL"]

            self.canvas.create_image(
                hurtbox[0].x + 64,
                hurtbox[0].y + 128,
                image=john
            )
        else:
            john = self.textures["johnJumpR"] if PLAYER.facing == 1 else self.textures["johnJumpL"]

            self.canvas.create_image(
                hurtbox[0].x + 64,
                hurtbox[0].y + 128,
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
