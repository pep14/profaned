import tkinter as tk
import os

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def tuple(self) -> tuple:
        return self.x, self.y
    

DEBUG = False

GRAVITY = -2
FRICTION = 0.8

MAXHP = 10
HURT_COOLDOWN = 10
HURT_TIME = 0

DASH_COOLDOWN = 15
DASH_SPEED = 28
DASH_TIME = 14

JUMP_STRENGTH = 25
PLR_SPEED = 3
STEP_TIME = 8

ATTACK_COOLDOWN = 15
ATTACK_TIME = 10

WINDOW_DIMENSIONS = Vector2(1280, 720)
WINDOW_BORDERS = 80