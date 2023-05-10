from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import pandas as pd

knn = KNeighborsRegressor(n_neighbors=2, weights="distance")

X = (58.0, 97.0)
y = ({'n': 5, 'i': 5}, {'n': 5, 'i': 20})

knn.fit(
    np.array(X).reshape(-1, 1),
    pd.DataFrame(y, columns=["n", "i"])
)



print(pd.DataFrame(knn.predict([[96]])))