import pyray
from raylib import colors


class Ball:
    def __init__(self, source: str, position: pyray.Vector2 = pyray.Vector2(0, 0),
                 direction: pyray.Vector2 = None,
                 radius: int = 30):
        img = pyray.load_image(source)
        self.texture = pyray.load_texture_from_image(img)
        self.texture.width = radius
        self.texture.height = radius
        self.direction = direction
        if direction is None:
            self.direction = pyray.Vector2(4, 4)
        self.position = position
        self.radius = radius
        pyray.unload_image(img)

    def draw(self, v: pyray.Vector2 = None):
        if v is None:
            v = self.position
        pyray.draw_texture(self.texture, int(v.x), int(v.y), colors.WHITE)

    def move(self):
        self.position.x += self.direction.x
        self.position.y += self.direction.y
        if self.position.x <= 0:
            self.direction.x *= -1
        if self.position.x >= 800 - self.texture.width:
            self.direction.x *= -1
        if self.position.y <= 0:
            self.direction.y *= -1
        if self.position.y >= 600 - self.texture.height:
            self.direction.y *= -1


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
        if self.position.x >= 600:
            self.position.x = 600
            self.u.x *= -.7

    def add(self, x: float):
        self.u.x += x


def main():
    pyray.init_window(800, 600, "Task-1")
    pyray.set_target_fps(60)
    ball1 = Ball('basketball.png', position=pyray.Vector2(100, 300),
                 direction=pyray.Vector2(2, 0))
    ball2 = Ball('basketball.png', position=pyray.Vector2(500, 300),
                 direction=pyray.Vector2(-2, 0))
    while not pyray.window_should_close():
        pyray.begin_drawing()
        pyray.clear_background(colors.BLACK)
        ball1.move()
        ball2.move()

        ball1.draw()
        ball2.draw()
        pyray.end_drawing()
    pyray.close_window()


if __name__ == '__main__':
    main()
