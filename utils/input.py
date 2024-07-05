import keyboard

class Input:
  @staticmethod
  def get_key(key:str)->bool:
    return keyboard.is_pressed(key)

  @staticmethod
  @property
  def key():
    return keyboard.read_key()
