from typing import Any

from scene.utils import getKey

class Scene:
  sceneName:str
  manager:Any # 임포트 에러 이슈

  def __init__(self):
    pass

  def render(self):
    print("Hello, World!")

  def _onPress(self, key):
    print(f"Pressed {getKey(key)}")
  def _onRelease(self, key):
    print(f"Release {getKey(key)}")
