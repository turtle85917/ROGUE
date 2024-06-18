from scene.manager import SceneManager

from scene.MiniMap.main import MiniMap

if __name__ == '__main__':
  sceneManager = SceneManager([MiniMap()])
  sceneManager.setDefaultScene(0)
  sceneManager.changeDefaultScene()
