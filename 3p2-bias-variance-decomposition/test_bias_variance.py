import numpy as np
from sklearn.linear_model import Ridge

from bias_variance import design_matrix, fit_ridge


def test_fit_ridge_matches_sklearn():
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 1, 25)
    t = np.sin(2 * np.pi * x) + rng.normal(0, 0.3, 25)
    Phi = design_matrix(x, np.linspace(0, 1, 24), 0.05)
    reference = Ridge(alpha=0.7, fit_intercept=False).fit(Phi, t)
    assert np.allclose(fit_ridge(Phi, t, 0.7), reference.coef_)
