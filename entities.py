from constants import *


def box_overlap(a, b):
    (a1, a2), (b1, b2) = a, b

    return (
        a1.x < b2.x and
        a2.x > b1.x and
        a1.y < b2.y and
        a2.y > b1.y
    )


class Entity(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vx = 0
        self.vy = 0


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


class Pider(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.maxhp = 30
        self.hp = self.maxhp
        self.stepT = 10
        self.walkframe = 0
        self.speed = 5

        self.idle = True

    @property
    def hurtbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 192, sy - 96),
            Vector2(sx + 192, sy + 96)
        )

    @property
    def passiveHitbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 160, sy - 64),
            Vector2(sx + 160, sy + 64)
        )

    @property
    def hitbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2 - 96
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 240, sy - 64),
            Vector2(sx + 80, sy + 64)
        )

    def update(self, px):
        targetx = px + 320

        dx = targetx - self.x

        if dx == 0:
            self.idle = True
            return
        
        self.idle = False

        if abs(dx) <= self.speed:
            self.x = targetx
        else:
            self.x += self.speed if dx > 0 else -self.speed

        if (nx := WINDOW_DIMENSIONS.x // 2 - 260) < self.x:
            self.idle = True
            self.x = nx
    
    def render(self, canvas: tk.Canvas, textures: dict):
        img = lambda n: textures[n]

        sprite = "piderwalk0" \
            if self.walkframe < self.stepT or self.idle else \
            "piderwalk1"

        self.walkframe = (self.walkframe + 1) % (self.stepT * 2)

        canvas.create_image(
            self.hurtbox[0].x + 192,
            self.hurtbox[0].y + 96,
            image=img(sprite)
        )