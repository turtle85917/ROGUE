from enum import IntEnum

class AnsiColor(IntEnum):
  Init      = 0
  Bold      = 1
  Italic    = 2
  Underline = 4

  TextBlack   = 30
  TextRed     = 31
  TextGreen   = 32
  TextYellow  = 33
  TextBlue    = 34
  TextMagenta = 35
  TextCyan    = 36
  TextWhite   = 37

  BackgroundBlack   = 40
  BackgroundRed     = 41
  BackgroundGreen   = 42
  BackgroundYellow  = 43
  BackgroundBlue    = 44
  BackgroundMagenta = 45
  BackgroundCyan    = 46
  BackgroundWhite   = 47
