from __future__ import annotations

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
    return Position(self.x * val, self.y * val)
  def __repr__(self):
    return f"({self.x}, {self.y})"

  @property
  def x(self):
    return self.__x
  @property
  def y(self):
    return self.__y
