from __future__ import annotations

from rendering.types.pixel import Pixel
from rendering.layer import Layer
from rendering.core import Rendering

WIDTH = 80
HEIGHT = 20

render = Rendering()

layer6 = Layer(WIDTH, HEIGHT)
layer5 = Layer(WIDTH, HEIGHT)

layer6.fill(Pixel.Test1)
layer5.fill(Pixel.Test2)

layer6.drawRect(10, 6, 7, 5)

render.pushLayers([layer5, layer6])

render.printLayer(layer6)
render.printLayer(layer5)

addedLayer = render.addLayers(layer6.width, layer6.height)

render.print(addedLayer)
render.print(render.subtractLayers(layer6.width, layer6.height, layer5, layer6))

render.printLayer(render.reverseLayer(layer6))

render.removeLayer(layer6)
render.pushLayer(render.reverseLayer(layer6))

render.print(render.addLayers(layer6.width, layer6.height))
