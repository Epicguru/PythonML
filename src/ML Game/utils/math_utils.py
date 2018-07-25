import math


def clamp(value: float, minimum: float, maximum: float) -> float:
    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def lerp(a, b, t, clamp_t: bool = True):
    return a + (b - a) * (t if not clamp_t else clamp(t, 0.0, 1.0))


class Vector2(tuple):

    def __new__(cls, x: float = 0.0, y: float = 0.0):
        n = tuple.__new__(cls, (x, y))
        n.x = x
        n.y = y
        return n

    def __init__(self, x: float = 0.0, y: float = 0.0):

        self.x = x
        self.y = y

        self._mag_dirty = True
        self._mag = 0.0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x: float):
        self.x = x
        self._mag_dirty = True

    def set_y(self, y: float):
        self.y = y
        self._mag_dirty = True

    def inc_x(self, xc: float):
        self.set_x(self.get_x() + xc)

    def inc_y(self, yc: float):
        self.set_y(self.get_y() + yc)

    def dec_x(self, xc: float):
        self.set_x(self.get_x() - xc)

    def dec_y(self, yc: float):
        self.set_y(self.get_y() - yc)

    def set(self, vector: "Vector2"):
        self.set_x(vector.get_x())
        self.set_y(vector.get_y())

    def magnitude(self):
        if self._mag_dirty:
            self._mag = math.sqrt(self.x**2 + self.y**2)
            self._mag_dirty = False
        return self._mag

    def normalize(self):
        mag = self.magnitude()
        self.set_x(self.get_x() / mag)
        self.set_y(self.get_y() / mag)

    def normalized(self) -> "Vector2":
        mag = self.magnitude()
        return Vector2(x=self.get_x() / mag, y=self.get_y() / mag)

    def __iadd__(self, other):
        if other is None:
            raise Exception("Cannot add None to this Vector2!")

        if isinstance(other, Vector2):
            self.set_x(self.get_x() + other.get_x())
            self.set_y(self.get_y() + other.get_y())
            return self
        else:
            raise TypeError("Cannot add object of type '%s' to a Vector2!" % type(other))

    def __isub__(self, other):
        if other is None:
            raise Exception("Cannot subtract None to this Vector2!")

        if isinstance(other, Vector2):
            self.set_x(self.get_x() - other.get_x())
            self.set_y(self.get_y() - other.get_y())
            return self
        else:
            raise TypeError("Cannot subtract object of type '%s' to a Vector2!" % type(other))

    def __add__(self, other):
        if other is None:
            raise Exception("Cannot add None to this Vector2!")

        if isinstance(other, Vector2):
            return Vector2(x=self.get_x() + other.get_x(), y=self.get_y() + other.get_y())
        else:
            raise TypeError("Cannot add object of type '%s' to a Vector2!" % type(other))

    def __sub__(self, other):
        if other is None:
            raise Exception("Cannot subtract None to this Vector2!")

        if isinstance(other, Vector2):
            return Vector2(x=self.get_x() - other.get_x(), y=self.get_y() - other.get_y())
        else:
            raise TypeError("Cannot subtract object of type '%s' to a Vector2!" % type(other))

    def __imul__(self, other):
        if other is None:
            raise Exception("Cannot multiply this Vector2 by None!")

        if isinstance(other, Vector2):
            self.set_x(self.get_x() * other.get_x())
            self.set_y(self.get_y() * other.get_y())
            return self
        elif isinstance(other, (float, int)):
            self.set_x(self.get_x() * other)
            self.set_y(self.get_y() * other)
            return self
        else:
            raise TypeError("Cannot multiply this Vector2 by object of type '%s'!" % type(other))

    def __mul__(self, other):
        if other is None:
            raise Exception("Cannot multiply this Vector2 by None!")

        if isinstance(other, Vector2):
            return Vector2(self.get_x() * other.get_x(), self.get_y() * other.get_y())
        elif isinstance(other, (float, int)):
            return Vector2(self.get_x() * other, self.get_y() * other)
            return self
        else:
            raise TypeError("Cannot multiply this Vector2 by object of type '%s'!" % type(other))

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.get_x() == other.get_x() and self.get_y() == other.get_y()
        return False

    def __itruediv__(self, other):
        if other is None:
            raise Exception("Cannot divide this Vector2 by None!")

        if isinstance(other, Vector2):
            self.set_x(self.get_x() / other.get_x())
            self.set_y(self.get_y() / other.get_y())
            return self
        elif isinstance(other, (float, int)):
            self.set_x(self.get_x() / other)
            self.set_y(self.get_y() / other)
            return self
        else:
            raise TypeError("Cannot divide this Vector2 by object of type '%s'!" % type(other))

    def __truediv__(self, other):
        if other is None:
            raise Exception("Cannot divide this Vector2 by None!")

        if isinstance(other, Vector2):
            return Vector2(self.get_x() / other.get_x(), self.get_y() / other.get_y())
        elif isinstance(other, (float, int)):
            return Vector2(self.get_x() / other, self.get_y() / other)
        else:
            raise TypeError("Cannot divide this Vector2 by object of type '%s'!" % type(other))

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)


VECTOR_ZERO = Vector2(0.0, 0.0)
VECTOR_ONE = Vector2(1.0, 1.0)
