from player import *
from pider import Pider
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
            "piderhp": tk.PhotoImage(file='./textures/piderhp.png').zoom(4, 4),
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

    def movementChecks(self):
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

    def hitboxChecks(self):
        global HURT_TIME

        if HURT_TIME > 0:
            HURT_TIME -= 1

        if PLR.attackT == ATTACK_TIME - 1 and box_overlap(PLR.hitbox, PIDER.hurtbox):
            PIDER.hp -= 1

        if PIDER.attackT == 1 and box_overlap(PLR.hurtbox, PIDER.hitbox) and not PLR.dashing:
            PLR.hp -= 1
            PLR.vx = -20
            HURT_TIME = HURT_COOLDOWN

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

    def run(self):
        if PLR.hp <= 0:
            self.destroy()
            return
        
        self.hitboxChecks()
        self.movementChecks()

        PLR.update()
        PIDER.update(PLR.x)
        self.render()

        self.after(20, self.run)

    def render(self):
        self.canvas.delete("all")

        self.canvas.create_image(640, 360, image=self.textures["background"])

        self.canvas.create_image(PLR.x + 640, 640, image=self.textures["plrshadow"])

        self.canvas.create_image(
            WINDOW_DIMENSIONS.x // 2, 
            WINDOW_DIMENSIONS.y - 75, 
            image=self.textures["piderhpbar"]
        )

        self.canvas.create_rectangle(
            WINDOW_DIMENSIONS.x // 2, 
            WINDOW_DIMENSIONS.y - 75, 
            WINDOW_DIMENSIONS.x // 2 + 10, 
            WINDOW_DIMENSIONS.y - 75 + 10, 
        )

        self.piderHpImage = tk.PhotoImage(file='./textures/piderhp.png').zoom(20 * PIDER.hp, 4)

        self.canvas.create_image(
            WINDOW_DIMENSIONS.x // 2, 
            WINDOW_DIMENSIONS.y - 31, 
            image=self.piderHpImage
        )

        for x in range(PLR.hp):
            self.canvas.create_image(32 + x * 32, 32, image=self.textures["hp"])
        
        for x in range(MAXHP - PLR.hp):
            self.canvas.create_image(32 + (PLR.hp + x) * 32, 32, image=self.textures["hpe"])

        PLR.render(self.canvas, self.textures)
        PIDER.render(self.canvas, self.textures)

if __name__ == "__main__":
    game = Profaned()
    game.run()
    game.mainloop()
