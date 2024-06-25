from typing import Optional, Any
import time

from pynput.keyboard import Listener

from player.core import Player

from rendering.layer import Layer
from rendering.main import Render

from scene.schema import Scene
from scene.constants import *
from scene.utils import setCursorShow, getKey, clearConsole

class SceneManager:
  __scenes__:list[Scene]

  __defaultSceneIndex:Scene
  __currentSceneIndex:int

  __globalVariables:dict[Any, Any]
  __globalListener:Listener

  __fps:float = 1. / 60 # frames per second
  __currentFrame:int = 0
  __lastTimeAt:int
  __isUpdating:bool = False

  player:Player
  layers:list[Layer] = []
  __render:Render

  def __init__(self, scenes:Optional[list[Scene]] = None):
    self.__scenes__ = scenes if scenes is not None else []
    self.__currentSceneIndex = 0
    self.__globalVariables = {}
    self.__globalListener = None

    self.layers = []
    self.player = Player()
    self.__render = Render()
    Layer.createNewLayers(self.layers, LAYERS, WIDTH, HEIGHT)

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

    # 전역 리스너 중단
    if self.__globalListener != None:
      self.__globalListener.stop()
    # 업데이트 중단
    if self.__isUpdating:
      self.__isUpdating = False

    self.clearAllLayers()

    self.__currentSceneIndex = sceneIndex
    self.currentScene.manager = self
    self.currentScene.render()

    # 씬이 업데이트가 가능하면 매 프레임마다 업데이트를 한다.
    if self.currentScene.updatable:
      self.__currentFrame = 0
      self.__lastTimeAt = time.time()
      self.__update()

  def setGlobalVariable(self, key:Any, value:Any):
    '''
    전역 변수를 설정합니다.

    @param key 키
    @param value 값
    '''
    self.__globalVariables[key] = value
  def setGlobalVariables(self, vars:dict[Any, Any]):
    '''
    전역 변수를 설정합니다.

    @param vars 키-값
    '''
    for k, v in vars.items():
      self.__globalVariables[k] = v
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

  def print(self):
    self.__render.print(self.__render.addLayers(WIDTH, HEIGHT, self.layers))
  def clearAllLayers(self):
    for layer in self.layers:
      layer.clear()

  @property
  def currentScene(self)->Scene:
    return self.__scenes__[self.__currentSceneIndex]
  @property
  def frame(self)->int:
    return self.__currentFrame

  def __update(self):
    '''
    업데이트 호출 시, 다음과 같은 과정을 거친다.

    - 해당 씬의 업데이트 함수 호출
    - 레이어 업데이트
    - 최종적으로 그린 후, 출력
    - 다음 프레임까지 대기 걸기
    '''
    while self.__isUpdating:
      self.__lastTimeAt = time.time()
      # 함수 호출
      self.currentScene.update()
      # 레이어 업데이트
      clearConsole()
      self.print()
      # 최종 작업
      self.__currentFrame += 1
      elasped = time.time() - self.__lastTimeAt
      time.sleep(max(0, self.__fps - elasped))
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
