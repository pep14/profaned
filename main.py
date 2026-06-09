import tkinter as tk
from entities import *
from keybinds import *


DEBUG = False

GRAVITY = -2
FRICTION = 0.8

DASH_COOLDOWN = 15
DASH_SPEED = 28
DASH_TIME = 14

JUMP_STRENGTH = 25
PLR_SPEED = 3
STEP_TIME = 8

ATTACK_COOLDOWN = 15
ATTACK_TIME = 10


KB = Keybinds(
    move_left="a",
    move_right="d",
    jump="space",
    dash="Shift_L",
    attack="k"
)

WINDOW_DIMENSIONS = Vector2(1280, 720)
WINDOW_BORDERS = 80
PLAYER = Player(0, 360, GRAVITY, FRICTION, WINDOW_DIMENSIONS, WINDOW_BORDERS)


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
        self.walkframe = 0
        self.textures = {
            "background": tk.PhotoImage(file="./textures/background.png").zoom(4, 4),
            "plrshadow": tk.PhotoImage(file='./textures/plrshadow60.png').zoom(5, 5),
            "johnR": tk.PhotoImage(file='./textures/R/plrsword.png').zoom(4, 4),
            "johnL": tk.PhotoImage(file='./textures/L/plrsword.png').zoom(4, 4),
            "johnSlideR": tk.PhotoImage(file='./textures/R/plrslide.png').zoom(4, 4),
            "johnSlideL": tk.PhotoImage(file='./textures/L/plrslide.png').zoom(4, 4),
            "johnJumpR": tk.PhotoImage(file='./textures/R/plrairborne.png').zoom(4, 4),
            "johnJumpL": tk.PhotoImage(file='./textures/L/plrairborne.png').zoom(4, 4),
            "johnAttackR": tk.PhotoImage(file='./textures/R/plrattack.png').zoom(4, 4),
            "johnAttackL": tk.PhotoImage(file='./textures/L/plrattack.png').zoom(4, 4),
            "johnWalk0R": tk.PhotoImage(file='./textures/R/plrwalk0.png').zoom(4, 4),
            "johnWalk0L": tk.PhotoImage(file='./textures/L/plrwalk0.png').zoom(4, 4),
            "johnWalk1R": tk.PhotoImage(file='./textures/R/plrwalk1.png').zoom(4, 4),
            "johnWalk1L": tk.PhotoImage(file='./textures/L/plrwalk1.png').zoom(4, 4),
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

        if KB.dash in self.keysDown and PLAYER.dashCD == 0 and PLAYER.grounded and not (PLAYER.dashing or PLAYER.attacking):
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

        if KB.attack in self.keysDown and PLAYER.attackCD == 0 and PLAYER.grounded and not (PLAYER.dashing or PLAYER.attacking):
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

        self.canvas.create_image(640, 360, image=self.textures["background"])

        hitbox = PLAYER.hitbox
        hurtbox = PLAYER.hurtbox

        self.canvas.create_image(PLAYER.x + 640, 640, image=self.textures["plrshadow"])

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
                    hurtbox[0].x + 128,
                    hurtbox[0].y + 128,
                    image=self.textures["johnAttackR"]
                )
            else:
                self.canvas.create_image(
                    hurtbox[0].x + 0,
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
            if PLAYER.vx == 0:
                john = self.textures["johnR"] if PLAYER.facing == 1 else self.textures["johnL"]
            elif self.walkframe < STEP_TIME:
                john = self.textures["johnWalk0R"] if PLAYER.facing == 1 else self.textures["johnWalk0L"]
                self.walkframe = (self.walkframe + 1) % (STEP_TIME * 2)
            else:
                john = self.textures["johnWalk1R"] if PLAYER.facing == 1 else self.textures["johnWalk1L"]
                self.walkframe = (self.walkframe + 1) % (STEP_TIME * 2)

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

        self.keysDown.add(event.keysym)

    def _keyReleased(self, event) -> None:
        self.keysDown.discard(event.keysym)

if __name__ == "__main__":
    game = Profaned()
    game.run()
    game.mainloop()
