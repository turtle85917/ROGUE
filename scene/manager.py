from typing import Optional, Any

from pynput.keyboard import Listener

from scene.schema import Scene
from scene.utils import setCursorShow, getKey

class SceneManager:
  __scenes__:list[Scene]

  __defaultSceneIndex:Scene
  __currentSceneIndex:int

  __globalVariables:dict[Any, Any]
  __globalListener:Listener

  def __init__(self, scenes:Optional[list[Scene]] = None):
    self.__scenes__ = scenes if scenes is not None else []
    self.__currentSceneIndex = 0
    self.__globalVariables = {}
    self.__globalListener = None

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
    self.__defaultSceneIndex = index

  def changeDefaultScene(self):
    '''
    기본 씬으로 전환합니다.
    '''
    self.changeScene(self.__defaultSceneIndex)
  def changeScene(self, sceneIndex:int):
    '''
    씬으로 전환합니다.

    @param sceneIndex 씬의 인덱스
    '''
    if len(self.__scenes__) <= sceneIndex:
      raise Exception("Not found scene")

    if self.__globalListener != None:
      self.__globalListener.stop()

    self.__currentSceneIndex = sceneIndex
    self.__scenes__[sceneIndex].manager = self
    self.__scenes__[sceneIndex].render()

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

  def listen(self):
    '''
    키보드 입력을 받기 시작합니다.
    '''
    try:
      currentScene = self.__scenes__[self.__currentSceneIndex]
      with Listener(
        on_press=self.__onPress,
        on_release=currentScene._onRelease,
        suppress=True
      ) as listener:
        self.__globalListener = listener
        self.__globalListener.join()
    except:
      self.__processQuit()
  def stopListen(self):
    self.__globalListener.stop()

  @property
  def currentSceneName(self)->int:
    return self.__scenes__[self.__currentSceneIndex].sceneName

  def __onPress(self, key):
    if getKey(key) == "q":
      self.__processQuit()
    else:
      currentScene = self.__scenes__[self.__currentSceneIndex]
      currentScene._onPress(key)
  def __processQuit(self):
    self.__running__ = False
    setCursorShow(True)
    self.__globalListener.stop()
