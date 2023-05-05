
from interval import interval
from functools import reduce

def closest_path(intervals : list[interval], limit) -> list[float]:
    if not len(intervals):
        return []
    
    values : list[list[int]] = [sorted([int(bounds[0]) for bounds in interv]) for interv in intervals]
    min  = reduce(lambda acc, list : acc + list[0], values, 0)
    if limit <= min: 
        return [v[0] for v in values]
    
    dp = [[0 for _ in range(limit + 1)] for _ in range(len(values))]
    last = [-1] * (limit + 1)

    for i in range(len(values[0])):
        if values[0][i] < limit:
            last[values[0][i]] = values[0][i]
            dp[0][values[0][i]] = values[0][i]

    for i in range(1, len(values)):
        current = [-1] * (limit + 1)
        for i_n in values[i]:
            for w in range(i_n, limit + 1):
                if last[w - i_n] > 0:
                    current[w] = max(current[w], last[w - i_n] + i_n)
                    dp[i][w] = current[w] - last[w - i_n]
            last = current
    return find_path_dp(dp)


def find_path_dp(dp):
    y = len(dp) - 1
    x = len(dp[y]) - 1 - dp[y][::-1].index(max(dp[y]))
    arr = []
    while y >= 0:
        arr.append(dp[y][x])
        x -= dp[y][x]
        y-=1
    arr.reverse()
    return arr
v = closest_path([interval([3, 4], [5, 7]), interval[2, 8], interval[6, 8], interval[2, 4], interval[6, 7]], 20)

print(v, sum(v))
