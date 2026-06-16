def box_overlap(a, b):
    (a1, a2), (b1, b2) = a, b

    return (
        a1.x < b2.x and
        a2.x > b1.x and
        a1.y < b2.y and
        a2.y > b1.y
    )


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