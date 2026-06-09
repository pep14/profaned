class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self) -> tuple:
        return self.x, self.y


class Entity(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vx = 0
        self.vy = 0


class Player(Entity):
    def __init__(self, x, y, gravity: float, friction: float, window: Vector2, windowBorders: int):
        super().__init__(x, y)

        self.window = window
        self.gravity = gravity
        self.friction = friction
        self.windowBorders = windowBorders

        self.grounded = False
        self.facing = 1

        self.dashing = False
        self.attacking = False

        self.dashT = 0
        self.dashCD = 0

        self.attackT = 0
        self.attackCD = 0

    @property
    def hurtbox(self):
        sx = self.x + self.window.x // 2
        sy = self.window.y - self.y

        return (
            Vector2(sx - 64, sy - 256),
            Vector2(sx + 64, sy)
        )

    @property
    def hitbox(self):
        sx = self.x + self.window.x // 2 + 64 * self.facing
        sy = self.window.y - self.y

        return (
            Vector2(sx - 64, sy - 192),
            Vector2(sx + 64, sy - 64)
        )

    def attack(self):
        if not self.attacking:
            self.attacking = True

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        if self.y < self.windowBorders:
            self.y = self.windowBorders
            self.vy = 0
            self.grounded = True
        else:
            self.grounded = False

        min_x = -self.window.x // 2 + self.windowBorders + 64
        max_x = self.window.x // 2 - self.windowBorders - 64

        if self.x < min_x:
            self.x = min_x
            self.vx = max(0, self.vx)

        elif self.x > max_x:
            self.x = max_x
            self.vx = min(0, self.vx)

        # deadzone
        if abs(self.vx) < 0.4:
            self.vx = 0

        if not self.dashing:
            self.vx *= self.friction