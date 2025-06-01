import abc
import math

class Shape(abc.ABC):

    @abc.abstractmethod
    def area(self):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width: int = 0, height: int = 0):
        self._width = width
        self._height = height

    def area(self):
        self._area = self._width * self._height
        return self._area

    def get_width(self):
        return self._width
    def get_height(self):
        return self._height

    def set_width(self, width: int):
        if width < 0:
            raise RuntimeError("Width cannot be less than 0")
            return
        self._width = width

    def set_height(self, height: int):
        if height < 0:
            raise RuntimeError("Height cannot be less than 0")
            return
        self._height = height
            
class Circle(Shape):
    def __init__(self, radius: int = 0):
        self._radius = radius

    def area(self):
        self._area = math.pi * self._radius**2
        return self._area

    def get_radius(self):
        return self._radius

    def set_radius(self, radius: int):
        if radius < 0:
            raise RuntimeError("Radius cannot be less than 0")
            return
        self._radius = radius
