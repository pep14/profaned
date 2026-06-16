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

PLR = Player(-240, 360)
PIDER = Pider(400, 180)


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

        for filename in os.listdir("./textures/pider/"):
            self.textures[filename[0:-4]] = tk.PhotoImage(
                file="./textures/pider/%s" % filename
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
        
        if HURT_TIME > 0:
            HURT_TIME -= 1

        if HURT_TIME == 0 and box_overlap(PLR.hurtbox, PIDER.passiveHitbox):
            PLR.dashing = False
            PLR.hp -= 1
            PLR.vx = -20
            HURT_TIME = HURT_COOLDOWN

        for projectile in PIDER.projectiles:
            if HURT_TIME == 0 and box_overlap(PLR.hurtbox, projectile.hitbox):
                PLR.dashing = False
                PLR.hp -= 1
                PLR.vx = -20
                HURT_TIME = HURT_COOLDOWN


        if KB.jump in self.keysDown and PLR.grounded:
            PLR.vy = JUMP_STRENGTH

        if HURT_TIME == 0 and not  (PLR.attacking or PLR.dashing):
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
        PIDER.update(PLR.x)
        self.render()

        self.after(20, self.run)

    def render(self):
        self.canvas.delete("all")

        self.canvas.create_image(640, 360, image=self.textures["background"])

        self.canvas.create_image(PLR.x + 640, 640, image=self.textures["plrshadow"])

        for x in range(PLR.hp):
            self.canvas.create_image(32 + x * 32, 32, image=self.textures["hp"])
        
        for x in range(MAXHP - PLR.hp):
            self.canvas.create_image(32 + (PLR.hp + x) * 32, 32, image=self.textures["hpe"])

        PLR.render(self.canvas, self.textures)
        PIDER.render(self.canvas, self.textures)

        if DEBUG:
            if not PLR.dashing:
                self.canvas.create_rectangle(
                    PLR.hurtbox[0].x, PLR.hurtbox[0].y,
                    PLR.hurtbox[1].x, PLR.hurtbox[1].y,
                    outline="#ff0000"
                )

            if PLR.attacking:
                self.canvas.create_rectangle(
                    PLR.hitbox[0].x, PLR.hitbox[0].y,
                    PLR.hitbox[1].x, PLR.hitbox[1].y,
                    outline="#ffff00"
                )
            
            self.canvas.create_rectangle(
                PIDER.hurtbox[0].x, PIDER.hurtbox[0].y,
                PIDER.hurtbox[1].x, PIDER.hurtbox[1].y,
                outline="#ff00ff"
            )

            self.canvas.create_rectangle(
                PIDER.passiveHitbox[0].x, PIDER.passiveHitbox[0].y,
                PIDER.passiveHitbox[1].x, PIDER.passiveHitbox[1].y,
                outline="#00ffff"
            )

            self.canvas.create_rectangle(
                PIDER.hitbox[0].x, PIDER.hitbox[0].y,
                PIDER.hitbox[1].x, PIDER.hitbox[1].y,
                outline="#0000ff"
            )

            for projectile in PIDER.projectiles:
                self.canvas.create_rectangle(
                    projectile.hitbox[0].x, projectile.hitbox[0].y,
                    projectile.hitbox[1].x, projectile.hitbox[1].y,
                    outline="#0000ff"
                )


if __name__ == "__main__":
    game = Profaned()
    game.run()
    game.mainloop()