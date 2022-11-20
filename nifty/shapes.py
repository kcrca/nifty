import cairo
import numpy as np
from cairo import Surface

from colour import Color
from nifty.fuzz import Fuzzer, Fuzzers


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


def draw_line(surface, coords, color):
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(*color.rgba)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(1.5)
    ctx.move_to(coords[0][0], coords[0][1])
    for i in range(1, len(coords)):
        ctx.line_to(coords[i][0], coords[i][1])
    ctx.stroke()


def chaikin(surface: Surface, coords, color: Color, coord_fuzzer: Fuzzer[float] = None, refinements=5):
    coords = np.array(coords)
    if coord_fuzzer is None:
        coord_fuzzer = Fuzzers.no_fuzz()

    base_color = color.darker()
    base_color.alpha = 0.1
    draw_line(surface, coords, base_color)
    for i in range(refinements):
        Q = coords.repeat(2, axis=0)
        R = np.empty_like(Q)
        R[0] = Q[0]
        R[2::2] = Q[1:-1:2]
        R[1:-1:2] = Q[2::2]
        R[-1] = Q[-1]
        coords = np.array(tuple(q * coord_fuzzer(0.75) for q in Q)) + np.array(tuple(r * coord_fuzzer.fuzz(0.25) for r in R))
        # print(i, coords)
        # print(i, Q * coord_fuzzer.fuzz(0.75) + R * coord_fuzzer.fuzz(0.25))

    draw_line(surface, coords, color)

    return coords
