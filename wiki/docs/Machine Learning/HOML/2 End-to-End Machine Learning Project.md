---
title: 2 End-to-End Machine Learning Project
---

### Fine Tune Model

#### Grid Search

Search the hyperparameters manually is very tedious, `GridSearchCV` may search for you after tell it which *hyperparameters* you want it to experiment with, and what *values* to try out, and it will evaluate all the possible combinations of hyperparameter values, using cross-validation.

```Python
from sklearn.model_selection import GridSearchCV
param_grid = [
{'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]}, 
{'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]}, 
]
forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5, 
                    scoring='neg_mean_squared_error')
grid_search.fit(housing_prepared, housing_labels)
```


!!! tip
    When you have no idea what value a hyperparameter should have, a simple approach is to try out consecutive powers of 10 or a smaller number if you want a more fine-grained search.