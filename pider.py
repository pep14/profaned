from piderProjectile import *


class Pider(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.maxhp = 30
        self.hp = self.maxhp
        self.stepT = 5
        self.walkframe = 0
        self.speed = 5

        self.state = A_NONE
        self.stationary = True
        self.ticksSinceLastProjectile = 0
        self.attackWindupT = 0
        self.attackT = 0

        self.projectiles: list[PiderProjectile] = []
        self.stateSpritesheet = {
            A_NONE: "piderwalk0",
            A_RANGED_ACTIVE: "piderflipped",
            A_MELEE_WINDUP: "piderattackwindup",
            A_MELEE_ACTIVE: "piderattack",
        }

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

    def moveToward(self, target):
        dx = target - self.x

        if dx == 0:
            self.stationary = True
            return
        
        self.stationary = False

        if abs(dx) <= self.speed:
            self.x = target
        else:
            self.x += self.speed if dx > 0 else -self.speed

        if (nx := WINDOW_DIMENSIONS.x // 2 - 260) < self.x:
            self.x = nx

    def update(self, plrX):
        # projectile updates
        if all(p.x < -WINDOW_DIMENSIONS.x // 2 for p in self.projectiles):
            self.projectiles = []

        for p in self.projectiles:
            p.update()
        
        # pider :3
        match self.state:
            case 0:
                self.state = random.choice(STATE_POOL)

            case 1:
                target = 380

                if self.x == target:
                    self.state = A_RANGED_ACTIVE
                    return

                self.moveToward(target)

            case 2:
                if len(self.projectiles) > PIDER_PROJECTILE_CAP - 1:
                    self.state = A_MELEE
                    return
            
                if self.ticksSinceLastProjectile > 25:
                    self.ticksSinceLastProjectile = 0
                    self.projectiles.append(
                        PiderProjectile(self.x - 96, self.y - 16)
                    )
                
                self.ticksSinceLastProjectile += 1

            case 3:
                target = plrX + 320

                if self.x <= target:
                    self.state = A_MELEE_WINDUP
                    return

                self.moveToward(target)

            case 4:
                self.attackWindupT += 1

                if self.attackWindupT >= PIDER_ATTACK_WINDUP:
                    self.state = A_MELEE_ACTIVE
                    self.attackWindupT = 0
                    return
            
            case 5:
                self.attackT += 1

                if self.attackT >= PIDER_ATTACK:
                    self.attackT = 0
                    self.state = A_NONE
    
    def render(self, canvas: tk.Canvas, textures: dict):
        img = lambda n: textures[n]

        if self.state in [A_MELEE, A_RANGED]:
            sprite = "piderwalk0" \
                if self.walkframe < self.stepT else \
                "piderwalk1"
            
            self.walkframe = (self.walkframe + 1) % (self.stepT * 2)

        else:
            sprite = self.stateSpritesheet[self.state]

        ox = 96 if self.state == A_MELEE_ACTIVE else 192
        oy = 96

        canvas.create_image(
            self.hurtbox[0].x + ox,
            self.hurtbox[0].y + oy,
            image=img(sprite)
        )

        for child in self.projectiles:
            child.render(canvas, textures)
