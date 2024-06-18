from typing import Optional, Any

from scene.schema import Scene

class SceneManager:
  __scenes__:list[Scene]

  __defaultScene:Scene
  __currentSceneIndex:int

  __globalVariables:dict[Any, Any]

  def __init__(self, scenes:Optional[list[Scene]] = None):
    self.__scenes__ = scenes if scenes is not None else []
    self.__currentSceneIndex = 0
    self.__globalVariables = {}

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
      raise Exception("Not found scene")
    self.__scenes__[sceneIndex].manager = self
    self.__scenes__[sceneIndex].render()
    self.__currentSceneIndex = sceneIndex

  def setGlobalVariable(self, key:Any, value:Any):
    '''
    전역 변수를 설정합니다.

    @param key 키
    @param value 값
    '''
    self.__globalVariables[key] = value
  def getGlobalVariable(self, key:Any)->Any:
    '''
    전역 변수를 가져옵니다.

    @param key 키
    '''
    return self.__globalVariables[key]

  @property
  def currentSceneName(self)->int:
    return self.__scenes__[self.__currentSceneIndex].sceneName
