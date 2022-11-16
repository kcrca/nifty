import cairo
from cairo import Surface
from colour import Color

from nifty.fuzz import Fuzzers


class Shapes:
    @staticmethod
    def bloom(surface: Surface, ul: tuple[float, float],
              lr: tuple[float, float], color: Color):
        w = lr[0] - ul[0]
        h = lr[1] - ul[1]
        base = [ul[0], lr[1]]
        mid1 = [ul[0] + w * 2, ul[1] + h * 25 / 30]
        mid2 = [ul[0] + w * 2, ul[1] + h * 2 / 30]
        end = [ul[0] + w, ul[1]]
        width_fuzz = Fuzzers.uniform(1, 0.5)
        color_fuzz = Fuzzers.color(0.1, 0.2, 0.1)
        ctx = cairo.Context(surface)
        base_range, mid1_range, mid2_range, end_range = w * 5 / 75, w * 50 / 75, w * 50 / 75, w * 275 / 75
        count = 120
        for i in range(count):
            c = color_fuzz.fuzz(color)
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
