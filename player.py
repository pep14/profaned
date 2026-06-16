from constants import *


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.hp = MAXHP
        self.hurtT = 0

        self.grounded = False
        self.facing = 1

        self.dashing = False
        self.attacking = False

        self.dashT = 0
        self.dashCD = 0

        self.attackT = 0
        self.attackCD = 0

        self.walkframe = 0

    @property
    def hurtbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 64, sy - 256),
            Vector2(sx + 64, sy)
        )

    @property
    def hitbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2 + 96 * self.facing
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 96, sy - 192),
            Vector2(sx + 96, sy - 64)
        )

    def attack(self):
        if not self.attacking:
            self.attacking = True

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        if self.y < WINDOW_BORDERS:
            self.y = WINDOW_BORDERS
            self.vy = 0
            self.grounded = True
        else:
            self.grounded = False

        min_x = -WINDOW_DIMENSIONS.x // 2 + WINDOW_BORDERS + 64
        max_x = WINDOW_DIMENSIONS.x // 2 - WINDOW_BORDERS - 64

        if self.x < min_x:
            self.x = min_x
            self.vx = max(0, self.vx)

        elif self.x > max_x:
            self.x = max_x
            self.vx = min(0, self.vx)

        if abs(self.vx) < 0.4:
            self.vx = 0

        if not self.dashing:
            self.vx *= FRICTION

    def render(self, canvas: tk.Canvas, textures: dict):
        img = lambda n: textures[n]

        if self.attacking:
            sprite = "plrattackR" if self.facing == 1 else "plrattackL"
            offset = (128, 128) if self.facing == 1 else (0, 128)

        elif self.dashing:
            sprite = "plrslideR" if self.facing == 1 else "plrslideL"
            offset = (64, 192)

        elif self.grounded:
            if self.vx == 0:
                sprite = "plrswordR" if self.facing == 1 else "plrswordL"
            else:
                sprite = ("plrwalk0R" if self.facing == 1 else "plrwalk0L") \
                    if self.walkframe < STEP_TIME else \
                    ("plrwalk1R" if self.facing == 1 else "plrwalk1L")

                self.walkframe = (self.walkframe + 1) % (STEP_TIME * 2)

            offset = (64, 128)

        else:
            sprite = "plrairborneR" if self.facing == 1 else "plrairborneL"
            offset = (64, 128)

        canvas.create_image(
            self.hurtbox[0].x + offset[0],
            self.hurtbox[0].y + offset[1],
            image=img(sprite)
        )
