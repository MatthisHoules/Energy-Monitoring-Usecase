from interval import interval
from functools import reduce

def interval_min(interval : interval) -> int:
    return int(interval[0][0])

def interval_max(interval : interval) -> int:
    return int(interval[len(interval) - 1][1])

def interval_bounds(interval : interval) -> tuple[int, int]:
    return (interval_min(interval), interval_max(interval))

def intervals_min(intervals : list[interval]) -> int:
    return sum(map(interval_min, intervals))

def intervals_max(intervals : list[interval]) -> int:
    return sum(map(interval_max, intervals))

def intervals_bounds(intervals : list[interval]) -> tuple[int, int]:
    return reduce(lambda acc, x : (acc[0] + x[0], acc[1] + x[1]), map(interval_bounds, intervals))


