import random
from abc import ABC
from typing import Callable, Generic, Iterable, TypeVar

from colour import Color

T = TypeVar('T')
Fuzz = Callable[[T], T]


class Fuzzer(ABC, Generic[T]):
    def __init__(self, fuzzer: Fuzz):
        self.fuzzer = fuzzer

    def fuzz(self, v: T) -> T:
        return self.fuzzer(v)

    def fuzzes(self, vs: Iterable[T]) -> tuple[T]:
        return tuple(self.fuzz(x) for x in vs)


class Fuzzers:
    @staticmethod
    def uniform(mid: float, range: float) -> Fuzzer:
        return Fuzzer(lambda v: v + random.uniform(mid - range, mid + range))

    @staticmethod
    def gauss(mid: float, stddev: float) -> Fuzzer:
        return Fuzzer(lambda v: v + random.gauss(mid, stddev))

    @staticmethod
    def ranged(low: float, high: float, range: float) -> Fuzzer:
        half = range / 2
        fuzzer = Fuzzers.uniform(-half, +half)

        def fuzz(v: float) -> float:
            nv = min(max(v, half), high - half)
            return fuzzer.fuzz(nv)

        return Fuzzer(fuzz)

    @staticmethod
    def scaled(scale: float, fuzzer: Fuzzer) -> Fuzzer:
        return Fuzzer(lambda v: scale * fuzzer.fuzz(v))

    @staticmethod
    def color(h_range: float, s_range: float, l_range: float) -> Fuzzer[Color]:
        h_fuzz = Fuzzers.ranged(0, 1, h_range)
        s_fuzz = Fuzzers.ranged(0, 1, s_range)
        l_fuzz = Fuzzers.ranged(0, 1, l_range)

        def fuzz(v: Color) -> Color:
            h, s, l = v.hsl
            return Color(hsl=(h_fuzz.fuzz(h), s_fuzz.fuzz(s), l_fuzz.fuzz(l)))

        return Fuzzer(fuzz)
