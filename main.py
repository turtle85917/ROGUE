from scene.manager import SceneManager

from scene.MiniMap.main import MiniMap
from scene.Room.main import Room

if __name__ == '__main__':
  sceneManager = SceneManager([
    MiniMap(),
    Room()
  ])
  sceneManager.setDefaultScene(0)
  sceneManager.changeDefaultScene()
