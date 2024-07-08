from typing import Any

class Scene:
  sceneName:str
  manager:Any # 임포트 에러 이슈

  def __init__(self): ...

  def render(self): ...
  def update(self): ...
