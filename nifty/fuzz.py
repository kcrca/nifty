import random
from abc import ABC
from typing import Callable, Iterable

Fuzz = Callable[[float], float]


class Fuzzer(ABC):
    def __init__(self, fuzzer: Fuzz):
        self.fuzzer = fuzzer

    def fuzz(self, v: float | Iterable[float]) -> float | tuple[float]:
        if isinstance(v, (float, int)):
            return self.fuzzer(v)
        return tuple(self.fuzzer(x) for x in v)


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
