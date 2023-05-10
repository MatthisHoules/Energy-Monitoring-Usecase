
import unittest
from interval import interval
from functools import reduce

def closest_path(intervals : dict[str, interval], target) -> dict[str, int]:
    """MCKP implementation. 
    
    Takes the minimal value of each interval ranges (ex [1, 4] U [8, 10] takes 1 and 8) and returns 
    the set of endpoint costs with the closest sum to the target 
    

    Args:
        intervals (dict[str, interval]): the map of interval {endpoint_name : interval_range}
        target (_type_): the target sum

    Returns:
        dict[str, int]: a map {endpoint_name : cost}
    """
    if target <= 0:
        return {}
    keys = list(intervals.keys())
    if not len(keys):
        return {}
    
    values : list[list[int]] = [sorted([int(bounds[0]) for bounds in interv]) for interv in intervals.values()]
    min  = reduce(lambda acc, list : acc + list[0], values, 0)
    if target <= min:
        return { keys[i] : values[i][0] for i in range(len(values)) }
    
    dp = [[-1 for _ in range(target + 1)] for _ in range(len(values))]
    last = [-1] * (target + 1)

    for i in range(len(values[0])):
        if values[0][i] < target:
            last[values[0][i]] = values[0][i]
            dp[0][values[0][i]] = values[0][i]

    for i in range(1, len(values)):
        current = [-1] * (target + 1)
        for i_n in values[i]:
            for w in range(i_n, target + 1):
                if last[w - i_n] > 0:
                    current[w] = max(current[w], last[w - i_n] + i_n)
                    dp[i][w] = current[w] - last[w - i_n]
        last = current

    
    return find_path_dp(dp, keys)


def find_path_dp(dp: list[list[int]], endpoints_name : list[str]) -> dict[str, int]:
    """backtracks the dynamic programming array and assigns each cost to the endpoint name

    Args:
        dp (list[list[int]]): the dp array[x][y]
        endpoints_name (list[str]): the endpoints_name[x]

    Returns:
        dict[str, int]: a map {endpoint_name : cost}
    """
    y = len(dp) - 1
    x = len(dp[y]) - 1
    while dp[y][x] < 0: 
        x -= 1
    arr = {}
    while y >= 0:
        arr[endpoints_name[y]] = dp[y][x]
        x -= dp[y][x]
        y -= 1
    return arr


class TestMCKP(unittest.TestCase):

    def test_lower(self):
        self.assertEqual(closest_path({"a":interval[3], "b": interval[5]}, 2), {"a":3, "b":5})

    def test_equal_min(self):
        self.assertEqual(closest_path({"a":interval[3], "b": interval[5]}, 8), {"a":3, "b":5})

    def test_between(self):
        self.assertEqual(closest_path({"a": interval(3, 4), "b": interval(4, 5), "c": interval(2, 6), "d": interval(7, 10)}, 18), {"a": 4, "b": 5, "c": 2, "d":7 })

    def test_equal_max(self):
        self.assertEqual(closest_path({"a":interval(3, 4), "b":interval(4, 5), "c": interval(2, 6), "d":interval(7, 10)}, 25), {"a":4, "b":5, "c":6, "d":10})

    def test_higher(self):
        self.assertEqual(closest_path({"a": interval(3, 4), "b": interval(4, 5), "c":interval(2, 6), "d": interval(7, 10)}, 35), {"a": 4, "b": 5, "c": 6, "d": 10})

    def test_empty_with_value(self):
        self.assertEqual(closest_path({}, 30), {})

    def test_empty_no_value(self):
        self.assertEqual(closest_path({}, -1), {})

    def test_no_value(self):
        self.assertEqual(closest_path({"a": interval[3], "b": interval[5]}, -1), {})


if __name__ == '__main__':
    unittest.main()    