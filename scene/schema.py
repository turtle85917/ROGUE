from typing import Any

class Scene:
  sceneName:str
  manager:Any # 임포트 에러 이슈
  updatable:bool

  def __init__(self):
    pass

  def render(self):
    print("Hello, World!")
  def update(self):
    pass

  def _onPress(self, key):
    pass
  def _onRelease(self, key):
    pass
