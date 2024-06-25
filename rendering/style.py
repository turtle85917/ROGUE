from rendering.types.ansi import AnsiColor

class Style:
  __styles:list[AnsiColor] = []
  __text:str

  __ESC = "\033"
  __close = f"{__ESC}[{AnsiColor.Init}m"

  def __init__(self, text:str, styles:list[AnsiColor]|AnsiColor|None = None):
    self.__text = text
    if styles != None:
      self.__styles = [styles] if isinstance(styles, AnsiColor) else styles

  def put(self, style:AnsiColor):
    self.__styles.append(style)
    return self

  def __repr__(self):
    head = f"{self.__ESC}["
    for style in self.__styles:
      head += f"{style}m;"
    head = head[:-1]
    return f"{head}{self.__text}{self.__close}"
