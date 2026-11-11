import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

from gaussian_process import kernel, posterior

X = np.linspace(-1, 1, 50)


def test_kernel_symmetric_positive_semi_definite():
    K = kernel(X, X)
    assert np.allclose(K, K.T)
    assert np.linalg.eigvalsh(K).min() > -1e-8


def test_posterior_matches_sklearn():
    x_train = np.array([-0.9, -0.4, 0.0, 0.3, 0.8])
    y_train = np.sin(2 * np.pi * x_train)
    mu, std = posterior(x_train, y_train, X)
    reference = GaussianProcessRegressor(RBF(0.4), alpha=0.05**2, optimizer=None).fit(x_train[:, None], y_train)
    mu_ref, std_ref = reference.predict(X[:, None], return_std=True)
    assert np.allclose(mu, mu_ref)
    assert np.allclose(std, std_ref)
