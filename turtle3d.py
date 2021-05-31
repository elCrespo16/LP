from vpython import *


def from_spherical_to_cartesian(r, vertical, horizontal):
    vertical = radians(vertical)
    horizontal = radians(horizontal)
    return vector(vector(r * cos(vertical) * cos(horizontal), r * sin(vertical), r * cos(vertical) * sin(horizontal)))


class Turtle3D:
    def __init__(self):
        self.horizontal = 0
        self.vertical = 0
        self.pos = vector(0, 0, 0)
        self.colored = vector(1, 0, 0)
        self.showable = True
        # paràmetres de l'escena
        scene.height = scene.width = 1000
        scene.autocenter = True
        scene.caption = """\nTo rotate "camera", drag with right button or Ctrl-drag.\nTo zoom, drag with middle 
        button or Alt/Option depressed, or use scroll wheel.\n  On a two-button mouse, middle is left + right.\nTo 
        pan left/right and up/down, Shift-drag.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate.\n """

        # posa els eixos de coordenades blancs
        cylinder(pos=vector(0, 0, 0), axis=vector(10, 0, 0), radius=0.1, color=color.white)
        cylinder(pos=vector(0, 0, 0), axis=vector(0, 10, 0), radius=0.1, color=color.white)
        cylinder(pos=vector(0, 0, 0), axis=vector(0, 0, 10), radius=0.1, color=color.white)

    def left(self, angle):
        self.horizontal += angle
        self.horizontal = self.horizontal % 360

    def right(self, angle):
        self.horizontal -= angle
        self.horizontal = self.horizontal % 360

    def up(self, angle):
        self.vertical += angle
        self.vertical = self.vertical % 360

    def down(self, angle):
        self.vertical -= angle
        self.vertical = self.vertical % 360

    def color(self, r, g, b):
        self.colored = [r, g, b]

    def show(self):
        self.showable = True

    def hide(self):
        self.showable = False

    def home(self):
        self.pos = vector(0, 0, 0)

    def forward(self, mida):
        start = vector(self.pos.x, self.pos.y, self.pos.z)
        self.pos += from_spherical_to_cartesian(mida, self.vertical, self.horizontal)
        if self.showable:
            self.print_movement(start, self.pos)

    def backward(self, mida):
        start = vector(self.pos.x, self.pos.y, self.pos.z)
        self.pos -= from_spherical_to_cartesian(mida, self.vertical, self.horizontal)
        if self.showable:
            self.print_movement(start, self.pos)

    def print_movement(self, start, finish):
        sphere(pos=start, radius=0.1, color=color.red)
        sphere(pos=finish, radius=0.1, color=color.red)
        cylinder(pos=start, axis=finish - start, radius=0.1, color=self.colored)


turtle = Turtle3D()
for i in range(4):
    turtle.forward(9)
    turtle.left(90)


def cercle(mida, costats):
    for i in range(1, costats):
        turtle.forward(mida)
        turtle.left(360 / costats)


def espiral(i):
    if i > 0:
        cercle(1, 12)
        turtle.up(5)
        espiral(i - 1)


espiral(5)
