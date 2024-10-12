import random

import pyray
from raylib import colors

WIDTH = 800
HEIGHT = 800

balls = []


class Ball:
    def __init__(self, source: str, position: pyray.Vector2 = pyray.Vector2(0, 0),
                 direction: pyray.Vector2 = None,
                 radius: int = 30):
        img = pyray.load_image(source)
        self.texture = pyray.load_texture_from_image(img)
        self.texture.width = radius * 2
        self.texture.height = radius * 2
        self.direction = direction
        if direction is None:
            self.direction = pyray.Vector2(4, 4)
        self.position = position
        self.radius = radius
        pyray.unload_image(img)

    def draw(self, v: pyray.Vector2 = None):
        if v is None:
            v = self.position
        pyray.draw_texture(self.texture, int(v.x), int(v.y) - 15, colors.WHITE)

    def move(self):
        self.position.x += self.direction.x
        self.position.y += self.direction.y
        if self.position.x <= 0:
            self.direction.x *= -1
        if self.position.x >= WIDTH - self.texture.width:
            self.direction.x *= -1
        if self.position.y <= 0:
            self.direction.y *= -1
        if self.position.y >= HEIGHT - self.texture.height:
            self.direction.y *= -1

        for ball in balls:
            if ball.position != self.position:
                if check_collision(self, ball):
                    self.direction, ball.direction = ball.direction, self.direction


def check_collision(ball1: Ball, ball2: Ball) -> bool:
    center1 = pyray.Vector2(ball1.position.x, ball1.position.y)
    center2 = pyray.Vector2(ball2.position.x, ball2.position.y)
    return pyray.check_collision_circles(center1, ball1.radius, center2, ball2.radius)


class Platform:
    def __init__(self, position: pyray.Vector2 = pyray.Vector2(500, 500)):
        self.position = position
        self.u = pyray.Vector2(0, 0)

    def draw(self, v: pyray.Vector2 = None):
        if v is None:
            v = self.position
        pyray.draw_rectangle(int(v.x), int(v.y), 200, 30, colors.RED)

    def tick(self):
        if self.u.x > 0:
            self.u.x -= .5
        elif self.u.x < 0:
            self.u.x += .5

        if 0.5 > self.u.x > -0.5:
            self.u.x = 0
        self.position.x += self.u.x

        if self.position.x <= 0:
            self.position.x = 0
            self.u.x *= -.7
        if self.position.x >= WIDTH - 200:
            self.position.x = WIDTH - 200
            self.u.x *= -.7

        for ball in balls:
            if self.check_collision(ball):
                ball.direction.x *= -1
                ball.direction.y *= -1

    def add(self, x: float):
        self.u.x += x

    def check_collision(self, ball: Ball) -> bool:
        center1 = pyray.Vector2(ball.position.x, ball.position.y)
        return pyray.check_collision_circle_rec(center1, ball.radius,
                                                pyray.Rectangle(self.position.x, self.position.y, 200, 30))


def main():
    pyray.init_window(WIDTH, HEIGHT, "Balls")
    pyray.set_target_fps(60)
    platform = Platform()
    for i in range(1):
        new_pos = pyray.Vector2(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100))
        ok = True
        while not ok:
            new_pos = pyray.Vector2(random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100))
            for ball in balls:
                if pyray.check_collision_circles(ball.position, 80, new_pos, 80):
                    ok = False
                    break
        balls.append(
            Ball('basketball.png', position=new_pos,
                 direction=pyray.Vector2(random.randint(100, 400) * random.choice([1, -1]) / 100,
                                         random.randint(100, 400) * random.choice([1, -1]) / 100))
        )

    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(colors.BLACK)

        if pyray.is_key_down(pyray.KeyboardKey.KEY_D):
            platform.add(1)
        if pyray.is_key_down(pyray.KeyboardKey.KEY_A):
            platform.add(-1)
        platform.tick()

        for ball in balls:
            ball.move()
            ball.draw()

        platform.draw()

        pyray.end_drawing()
    pyray.close_window()


if __name__ == '__main__':
    main()
