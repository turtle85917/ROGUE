import os

from pynput.keyboard import Key, KeyCode

def clearConsole():
  '''
  콘솔창을 클리어합니다.
  '''
  os.system('cls')
  setCursorShow(False)
  print('\033[0;0H')

def setCursorShow(isShow:bool):
  '''
  커서를 보여줄지 결정합니다.

  @param isShow 보여주기 여부
  '''
  print(f"\u001B[?25{'h' if isShow else 'l'}", end='')

def getKey(key:Key|KeyCode|str)->str|Key|None:
  return key.char if isinstance(key, KeyCode) else key
