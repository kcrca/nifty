import cairo
from colour import Color

from fuzz import Fuzzers

hue_fuzz = Fuzzers.ranged(0, 1, 0.1)
sat_fuzz = Fuzzers.ranged(0, 1, 0.2)
lum_fuzz = Fuzzers.ranged(0, 1, 0.1)


def variant(color):
    h, s, l = color.hsl
    nh = hue_fuzz.fuzz(h)
    sn = sat_fuzz.fuzz(s)
    ln = lum_fuzz.fuzz(l)
    return Color(hsl=(nh, sn, ln))


def bloomCairo():
    base = [100, 400]
    mid1 = [250, 350]
    mid2 = [250, 120]
    end = [175, 100]
    color = Color(hsl=(0.67, 1, 0.4))
    width_fuzz = Fuzzers.uniform(1, 0.5)
    with cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500) as surface:
        ctx = cairo.Context(surface)
        base_range, mid1_range, mid2_range, end_range = 5, 50, 50, 275
        count = 120
        for i in range(count):
            c = variant(color)
            ctx.set_source_rgb(*c.rgb)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_line_width(1 * width_fuzz.fuzz(1))
            ctx.move_to(*base)
            ctx.curve_to(*mid1, *mid2, *end)
            ctx.stroke()
            base[0] += base_range / count
            mid1[0] += mid1_range / count
            mid2[0] += mid2_range / count
            end[0] += end_range / count
        surface.write_to_png("out.png")


if __name__ == '__main__':
    bloomCairo()
