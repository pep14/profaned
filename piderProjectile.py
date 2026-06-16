from constants import *


class PiderProjectile(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.projectileSpeed = 25

    @property
    def hitbox(self):
        sx = self.x + WINDOW_DIMENSIONS.x // 2
        sy = WINDOW_DIMENSIONS.y - self.y

        return (
            Vector2(sx - 8, sy - 8),
            Vector2(sx + 8, sy + 8)
        )

    def update(self):
        self.x -= self.projectileSpeed

    def render(self, canvas: tk.Canvas, textures: dict):
        img = lambda n: textures[n]

        canvas.create_image(
            self.hitbox[0].x + 8,
            self.hitbox[0].y + 8,
            image=img("piderprojectile")
        )