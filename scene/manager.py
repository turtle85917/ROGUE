from typing import Optional, Any

import time
import curses
from _types.CurseWindow import CursesWindow

from object.player.core import Player

from rendering.layer import Layer
from rendering.main import Render

from scene.schema import Scene
from scene.constants import *

class SceneManager:
  __scenes__:list[Scene]

  __defaultSceneIndex:Scene
  __currentSceneIndex:int

  __globalVariables:dict[Any, Any]

  __currentFrame:int = 0
  __isUpdating:bool = False

  player:Player
  layers:list[Layer] = []

  __render:Render
  __window:CursesWindow
  pressedKey:str|None

  def __init__(self, scenes:Optional[list[Scene]] = None):
    self.__scenes__ = scenes if scenes is not None else []
    self.__currentSceneIndex = 0
    self.__globalVariables = {}

    self.layers = []
    self.player = Player()

    self.__window = curses.initscr()
    self.__render = Render(self.__window)

    # 윈도우 기본 옵션
    self.__window.keypad(True)
    self.__window.nodelay(True)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)

    # 색상 팔레트 초기화
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, 255):
      curses.init_pair(i + 1, i, -1)

    # 레이어 초기화
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

    # 업데이트 중단
    if self.__isUpdating:
      self.__isUpdating = False

    # 현재 씬 체크 및 화면 초기화
    self.__currentSceneIndex = sceneIndex
    self.clearAllLayers()

    # 매니저 할당
    self.currentScene.manager = self

    self.currentScene.render()

    # 매 프레임마다 업데이트를 한다.
    self.__currentFrame = 0
    self.__update()

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
    self.__isUpdating = True
    while self.__isUpdating:
      # 키 입력 처리
      key = self.__window.getch()
      self.__checkPressedKey(key)
      # 종료 시도
      if self.pressedKey == 'q' or self.pressedKey == "esc":
        self.__processQuit()
      #self.__window.erase()
      # 함수 호출
      self.currentScene.update()
      self.__window.refresh()
      # 레이어 업데이트
      self.__render.print(self.__render.addLayers(WIDTH, HEIGHT, self.layers))
      # 최종 작업
      self.__currentFrame += 1
      time.sleep(0.01)
  def __checkPressedKey(self, key:int):
    match key:
      case curses.KEY_LEFT:
        self.pressedKey = "left"
      case curses.KEY_RIGHT:
        self.pressedKey = "right"
      case curses.KEY_UP:
        self.pressedKey = "up"
      case curses.KEY_DOWN:
        self.pressedKey = "down"
      case 27: # esc keycode '27'
        self.pressedKey = "esc"
      case -1:
        self.pressedKey = None
      case _:
        if chr(key) == '\n': # pressed "enter"
          self.pressedKey = "enter"
        else:
          self.pressedKey = chr(key)

  def __processQuit(self):
    self.__running__ = False
    self.__isUpdating = False
    curses.curs_set(True)
