from vpython import *


def from_spherical_to_cartesian(r, vertical, horizontal):
    """
    Funcion que convierte coordenadas esfericas a un vector en coordenadas cartesianas
    :param r: Modulo del vector en coordenadas esfericas
    :param vertical: Angulo vertical en grados
    :param horizontal: Angulo Horizontal en grados
    :return: Vector con las coordenadas cartesianas asociadas a las coordenadas esfericas
    """
    vertical = radians(vertical)
    horizontal = radians(horizontal)
    return vector(vector(r * cos(vertical) * cos(horizontal), r * sin(vertical), r * cos(vertical) * sin(horizontal)))


class Turtle3D:
    """
    Clase que controla la escena grafica y la tortuga que imprime
    """
    def __init__(self):
        """
        Inicializacion de la clase
        """
        self.horizontal = 0
        self.vertical = 0
        self.pos = vector(0, 0, 0)
        self.colored = vector(1, 0, 0)
        self.showable = True

    def inicialize_scene(self):
        """
        Funcion para inicializar la ventana grafica
        :return: No devuelve nada
        """
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
        """
        Funcion que mueve el angulo horizontal de la tortuga hacia la izquierda angle grados
        :param angle: grados a mover la tortuga
        :return: No devuelve nada
        """
        self.horizontal += angle
        self.horizontal = self.horizontal % 360

    def right(self, angle):
        """
        Funcion que mueve el angulo horizontal de la tortuga hacia la derecha angle grados
        :param angle: grados a mover la tortuga
        :return: No devuelve nada
        """
        self.horizontal -= angle
        self.horizontal = self.horizontal % 360

    def up(self, angle):
        """
        Funcion que mueve el angulo vertical de la tortuga hacia la arriba angle grados
        :param angle: grados a mover la tortuga
        :return: No devuelve nada
        """
        self.vertical += angle
        self.vertical = self.vertical % 360

    def down(self, angle):
        """
        Funcion que mueve el angulo vertical de la tortuga hacia la abajo angle grados
        :param angle: grados a mover la tortuga
        :return: No devuelve nada
        """
        self.vertical -= angle
        self.vertical = self.vertical % 360

    def color(self, r, g, b):
        """
        Funcion que cambia el color del que pinta la tortuga
        :param r: Red component [0...1]
        :param g: Green component [0...1]
        :param b: Blue component [0...1]
        :return: No devuelve nada
        """
        self.colored = vector(r, g, b)

    def show(self):
        """
        Funcion que hace que la tortuga pinte mientras se mueve
        :return: No devuelve nada
        """
        self.showable = True

    def hide(self):
        """
        Funcion que hace que la tortuga no pinte mientras se mueve
        :return:
        """
        self.showable = False

    def home(self):
        """
        Funcion que mueve la tortuga al origen de coordenadas
        :return: No devuelve nada
        """
        self.pos = vector(0, 0, 0)

    def forward(self, mida):
        """
        Funcion que hace que la tortuga se mueva a hacia donde esta mirando
        :param mida: Distancia que tiene que recorrer
        :return: No devuelve nada
        """
        start = vector(self.pos.x, self.pos.y, self.pos.z)
        self.pos += from_spherical_to_cartesian(mida, self.vertical, self.horizontal)
        if self.showable:
            self.print_movement(start, self.pos)

    def backward(self, mida):
        """
        Funcion que hace que la tortuga se mueva a hacia el lado contrario a donde esta mirando
        :param mida: Distancia que tiene que recorrer
        :return: No devuelve nada
        """
        start = vector(self.pos.x, self.pos.y, self.pos.z)
        self.pos -= from_spherical_to_cartesian(mida, self.vertical, self.horizontal)
        if self.showable:
            self.print_movement(start, self.pos)

    def print_movement(self, start, finish):
        """
        Funcion para pintar los movimientos de la tortuga
        :param start: Inicio del movimiento
        :param finish: Final del movimiento
        :return: No devuelve nada
        """
        sphere(pos=start, radius=0.1, color=self.colored)
        sphere(pos=finish, radius=0.1, color=self.colored)
        cylinder(pos=start, axis=finish - start, radius=0.1, color=self.colored)

