class Entity:
    def __init__(self, pos, hitbox):
        self.x = pos[0]
        self.y = pos[1]
        self.hitbox = hitbox

    def setpos(self, x, y):
        self.x = x
        self.y = y