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
    def __init__(self, x, y, gravity, friction, window: Vector2):
        super().__init__(x, y)
        self.window = window
        self.gravity = gravity
        self.friction = friction
        self.grounded = False
        self.facing = 1
        self.dashing = False
        self.dashT = 0
        self.dashCD = 0
        self.attacking = False
        self.attackT = 0
        self.attackCD = 0

    @property
    def hurtbox(self):
        screen_x = self.x + self.window.x // 2
        screen_y = self.window.y - self.y
        
        return (
            Vector2(screen_x - 64, screen_y - 256),
            Vector2(screen_x + 64, screen_y - 0)
        )
    
    @property
    def hitbox(self):
        screen_x = self.x + self.window.x // 2 + 64 * self.facing
        screen_y = self.window.y - self.y

        return (
            Vector2(screen_x - 64, screen_y - 192),
            Vector2(screen_x + 64, screen_y - 64)
        )


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