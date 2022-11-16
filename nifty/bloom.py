import cairo
from colour import Color

from shapes import Shapes


def bloomCairo():
    with cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500) as surface:
        Shapes.bloom(surface, (100, 100), (175, 400), Color(hsl=(0.67, 1, 0.4)))
        surface.write_to_png("out.png")


if __name__ == '__main__':
    bloomCairo()
