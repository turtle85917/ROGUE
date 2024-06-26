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

  def out(self)->str:
    head = f"{self.__ESC}[{";".join(map(str, self.__styles))}m"
    return f"{head}{self.__text}{self.__close}"

  @staticmethod
  def bgColor(txColor:AnsiColor)->AnsiColor:
    if txColor // 10 != 3:
      raise ValueError("Invaild text color")
    return txColor + 10

  def __repr__(self)->str:
    return self.out()
