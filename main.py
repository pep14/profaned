import tkinter as tk
import os
from entities import *
from keybinds import *


KB = Keybinds(
    move_left="a",
    move_right="d",
    jump="space",
    dash="Shift_L",
    attack="k",
    debughit="h"
)

PLR = Player(0, 360, GRAVITY, FRICTION, WINDOW_DIMENSIONS, WINDOW_BORDERS, MAXHP)


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

        self.title("profaned")
        self.iconbitmap("./textures/icon.ico")

        self.walkframe = 0

        self.textures = {
            "background": tk.PhotoImage(file="./textures/background.png").zoom(4, 4),
            "plrshadow": tk.PhotoImage(file='./textures/plrshadow60.png').zoom(5, 5),

            "hp": tk.PhotoImage(file='./textures/hitpoint.png').zoom(4, 4),
            "hpe": tk.PhotoImage(file='./textures/hitpoint_empty.png').zoom(4, 4),
        }

        for filename in os.listdir("./textures/R/"):
            self.textures["%sR" % filename[0:-4]] = tk.PhotoImage(
                file="./textures/R/%s" % filename
            ).zoom(4, 4)

        for filename in os.listdir("./textures/L/"):
            self.textures["%sL" % filename[0:-4]] = tk.PhotoImage(
                file="./textures/L/%s" % filename
            ).zoom(4, 4)

        self.keysDown = set()
        self.bind("<KeyPress>", self._keyPressed)
        self.bind("<KeyRelease>", self._keyReleased)

    def _keyPressed(self, event):
        self.keysDown.add(event.keysym)

    def _keyReleased(self, event):
        self.keysDown.discard(event.keysym)

    def run(self):
        global HURT_TIME

        if PLR.hp <= 0:
            self.destroy()
            return

        if KB.debughit in self.keysDown and HURT_TIME == 0:
            PLR.hp -= 1
            HURT_TIME = HURT_COOLDOWN
        
        if HURT_TIME > 0:
            HURT_TIME -= 1

        if KB.jump in self.keysDown and PLR.grounded:
            PLR.vy = JUMP_STRENGTH

        if not (PLR.attacking or PLR.dashing):
            if KB.move_left in self.keysDown:
                PLR.vx -= PLR_SPEED
                PLR.facing = -1

            if KB.move_right in self.keysDown:
                PLR.vx += PLR_SPEED
                PLR.facing = 1

        PLR.dashCD = max(0, PLR.dashCD - 1)
        PLR.attackCD = max(0, PLR.attackCD - 1)

        if KB.dash in self.keysDown \
           and PLR.dashCD == 0 \
           and PLR.grounded \
           and not (PLR.dashing or PLR.attacking):

            PLR.dashing = True
            PLR.dashT = DASH_TIME
            PLR.dashCD = DASH_COOLDOWN
            PLR.vx = PLR.facing * DASH_SPEED

        if PLR.dashing:
            PLR.vx = PLR.facing * DASH_SPEED
            PLR.dashT -= 1
            if PLR.dashT <= 0:
                PLR.dashing = False

        if KB.attack in self.keysDown \
           and PLR.attackCD == 0 \
           and PLR.grounded \
           and not (PLR.dashing or PLR.attacking):

            PLR.attacking = True
            PLR.attackT = ATTACK_TIME
            PLR.attackCD = ATTACK_COOLDOWN

        if PLR.attacking:
            PLR.attackT -= 1
            if PLR.attackT <= 0:
                PLR.attacking = False

        PLR.update()
        self.render()

        self.after(20, self.run)

    def render(self):
        self.canvas.delete("all")

        plrHitbox = PLR.hitbox
        plrHurtbox = PLR.hurtbox

        self.canvas.create_image(640, 360, image=self.textures["background"])
        self.canvas.create_image(PLR.x + 640, 640, image=self.textures["plrshadow"])

        for x in range(PLR.hp):
            self.canvas.create_image(32 + x * 32, 32, image=self.textures["hp"])
        
        for x in range(MAXHP - PLR.hp):
            self.canvas.create_image(32 + (PLR.hp + x) * 32, 32, image=self.textures["hpe"])

        img = lambda n: self.textures[n]

        if PLR.attacking:
            sprite = "plrattackR" if PLR.facing == 1 else "plrattackL"
            offset = (128, 128) if PLR.facing == 1 else (0, 128)

        elif PLR.dashing:
            sprite = "plrslideR" if PLR.facing == 1 else "plrslideL"
            offset = (64, 192)

        elif PLR.grounded:
            if PLR.vx == 0:
                sprite = "plrswordR" if PLR.facing == 1 else "plrswordL"
            else:
                sprite = ("plrwalk0R" if PLR.facing == 1 else "plrwalk0L") \
                    if self.walkframe < STEP_TIME else \
                    ("plrwalk1R" if PLR.facing == 1 else "plrwalk1L")

                self.walkframe = (self.walkframe + 1) % (STEP_TIME * 2)

            offset = (64, 128)

        else:
            sprite = "plrairborneR" if PLR.facing == 1 else "plrairborneL"
            offset = (64, 128)

        self.canvas.create_image(
            plrHurtbox[0].x + offset[0],
            plrHurtbox[0].y + offset[1],
            image=img(sprite)
        )

        if DEBUG:
            if not PLR.dashing:
                self.canvas.create_rectangle(
                    plrHurtbox[0].x, plrHurtbox[0].y,
                    plrHurtbox[1].x, plrHurtbox[1].y,
                    outline="#ff0000"
                )

            if PLR.attacking:
                self.canvas.create_rectangle(
                    plrHitbox[0].x, plrHitbox[0].y,
                    plrHitbox[1].x, plrHitbox[1].y,
                    outline="#ffff00"
                )


if __name__ == "__main__":
    game = Profaned()
    game.run()
    game.mainloop()