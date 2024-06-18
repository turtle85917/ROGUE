from typing import Optional

from scene.schema import Scene

class SceneManager:
  __scenes__:list[Scene]

  __defaultScene:Scene
  __currentSceneIndex:int

  def __init__(self, scenes:Optional[list[Scene]] = None):
    self.__scenes__ = scenes if scenes is not None else []
    self.__currentSceneIndex = 0

  def render(self, scene:Scene):
    '''
    씬 목록에 씬을 추가합니다.

    @param scene 추가할 씬
    '''
    if scene not in self.__scenes__:
      self.__scenes__.append(scene)
    return self
  def setDefaultScene(self, index:int):
    '''
    기본 씬을 지정합니다.

    @param index 씬의 인덱스
    '''
    self.__defaultScene = self.__scenes__[index]

  def changeDefaultScene(self):
    '''
    기본 씬으로 전환합니다.
    '''
    self.__defaultScene.manager = self
    self.__defaultScene.render()
    self.__currentSceneIndex = self.__scenes__.index(self.__defaultScene)
  def changeScene(self, sceneIndex:int):
    '''
    씬으로 전환합니다.

    @param sceneIndex 씬의 인덱스
    '''
    if len(self.__scenes__) <= sceneIndex:
      raise Exception("denied")
    self.__scenes__[sceneIndex].manager = self
    self.__scenes__[sceneIndex].render()
    self.__currentSceneIndex = sceneIndex

  @property
  def currentSceneName(self)->int:
    return self.__scenes__[self.__currentSceneIndex].sceneName
