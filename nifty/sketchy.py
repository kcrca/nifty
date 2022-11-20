import cairo

from colour import Color
from nifty.fuzz import Fuzzers
from shapes import chaikin


# Shapely library is probably useful when composing things

def sketchy():
    with cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500) as surface:
        coords = ((100, 100), (375, 250), (150, 200), (220, 400))
        color = Color(hsl=(0.67, 1, 0.4))
        fuzzer = Fuzzers.uniform(0, 0.025)
        for _ in range(5):
            chaikin(surface, coords, color, fuzzer, refinements=2)
        surface.write_to_png("out.png")


if __name__ == '__main__':
    sketchy()
