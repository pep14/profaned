class Dim2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self) -> tuple:
        return self.x, self.y
    

class Entity(Dim2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vx = 0
        self.vy = 0


class Player(Entity):
    def __init__(self, x, y, gravity, friction):
        super().__init__(x, y)
        self.gravity = gravity
        self.friction = friction
        self.grounded = False
        self.facing = 1
        self.dashCD = 0
        self.dashing = False
        self.dashTime = 0
        self.attacking = False

    def attack(self):
        self.attacking = True

    def update(self):
        self.vy += self.gravity

        self.x += self.vx
        self.y += self.vy

        if self.y < 0:
            self.y = 0
            self.vy = 0
            self.grounded = True
        else:
            self.grounded = False

        if not self.dashing:
            self.vx *= self.friction