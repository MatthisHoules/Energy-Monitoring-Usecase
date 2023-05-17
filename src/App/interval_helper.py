# External Imports
from interval import interval
from functools import reduce




def interval_min(interval : interval) -> int :
    """interval_min

        returns :
            min value of interval
    """

    return int(interval[0][0])
# def interval_min(interval : interval) -> int



def interval_max(interval : interval) -> int :
    """interval_max

        returns :
            max value of interval
    """

    return int(interval[len(interval) - 1][1])
# def interval_max(interval : interval) -> int



def interval_bounds(interval : interval) -> tuple[int, int] :
    """interval_bounds

        returns :
            tuple that contains : 
                [0] : min value of interval
                [1] : max value of interval
    """

    return (interval_min(interval), interval_max(interval))
#def interval_bounds(interval : interval) -> tuple[int, int]



def intervals_min(intervals : list[interval]) -> int :
    """intervals_min

        returns :
            return sum of intervals min values
    """

    return sum(map(interval_min, intervals))
# def intervals_min(intervals : list[interval]) -> int



def intervals_max(intervals : list[interval]) -> int :
    """intervals_min

        returns :
            return sum of intervals max values
    """
        
    return sum(map(interval_max, intervals))
# def intervals_max(intervals : list[interval]) -> int



def intervals_bounds(intervals : list[interval]) -> tuple[int, int] :
    """intervals_bounds

        returns :
            bounds of multiple intervals
    """

    return reduce(lambda acc, x : (acc[0] + x[0], acc[1] + x[1]), map(interval_bounds, intervals))
# def intervals_bounds(intervals : list[interval]) -> tuple[int, int]

