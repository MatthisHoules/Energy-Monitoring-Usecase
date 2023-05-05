
from interval import interval
from functools import reduce
import pprint
def closest_path(intervals : list[interval], objective) -> list[float]:
    if not len(intervals):
        return []
    
    costs_classes : list[list[int]] = [sorted([int(bounds[0]) for bounds in interv]) for interv in intervals]
    min  = reduce(lambda acc, list : acc + sum(list), costs_classes, 0)
    if objective < min: 
        return [v[0] for v in costs_classes]
    
    dp = [[0 for _ in range(objective + 1)] for _ in range(len(costs_classes))]
    for i in range(len(costs_classes[0])):
        if costs_classes[0][i] < objective:
            dp[0][costs_classes[0][i]] = max(dp[0][costs_classes[0][i]], costs_classes[0][i])

    for i in range(1, len(costs_classes)):
        for j in range(len(costs_classes[i])):
            for k in range(costs_classes[i][j], objective + 1):
                dp[i][k] = max(dp[i][k-1], max(dp[i - 1][k], dp[i - 1][k - costs_classes[i][j]] + costs_classes[i][j]))
    return 0

print(closest_path([interval([2, 5], [6, 7]), interval[2, 8], interval[6, 8], interval[4, 2], interval[7, 6]], 4))
