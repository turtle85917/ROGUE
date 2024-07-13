from __future__ import annotations
from math import floor, sqrt

class Position:
  __x:int
  __y:int

  def __init__(self, x:int, y:int):
    self.__x = x
    self.__y = y

  def __add__(self, other:Position)->Position:
    '''
    두 위치를 합한 새로운 위치를 반환합니다.
    '''
    return Position(self.x + other.x, self.y + other.y)
  def __sub__(self, other:Position)->Position:
    '''
    두 위치를 뺀 새로운 위치를 반환합니다.
    '''
    return Position(self.x - other.x, self.y - other.y)
  def __mul__(self, val:int)->Position:
    '''
    위치와 숫자의 곱한 새로운 위치를 반환합니다.
    '''
    return Position(floor(self.x * val), floor(self.y * val))
  def __eq__(self, other:Position)->bool:
    '''
    두 위치가 같은지 확인합니다.
    '''
    return self.x == other.x and self.y == other.y
  def __ne__(self, other:Position)->bool:
    '''
    두 위치가 다른지 확인합니다.
    '''
    return self.x != other.x or self.y != other.y
  def __repr__(self)->str:
    return f"({self.x}, {self.y})"

  @property
  def x(self)->int:
    return self.__x
  @property
  def y(self)->int:
    return self.__y

  @property
  def magnitude(self)->int:
    return floor(sqrt((self.x + self.y) ** 2))
  @property
  def normalized(self)->Position:
    if self.magnitude == 0:
      return Position(self.x, self.y)
    return Position(self.x // self.magnitude, self.y // self.magnitude)
