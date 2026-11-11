import numpy as np


def kernel(x1, x2, length_scale=0.4):
    x1 = np.atleast_2d(x1).T
    x2 = np.atleast_2d(x2).T
    return np.exp(-0.5 * ((x1 - x2.T) / length_scale) ** 2)


def posterior(x_train, y_train, x_test, noise=0.05, length_scale=0.4):
    """Posterior predictive mean and standard deviation of the latent function at `x_test`."""
    K_train = kernel(x_train, x_train, length_scale) + noise**2 * np.eye(len(x_train))
    Ks = kernel(x_train, x_test, length_scale)
    L = np.linalg.cholesky(K_train)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_train))
    v = np.linalg.solve(L, Ks)
    cov = kernel(x_test, x_test, length_scale) - v.T @ v
    return Ks.T @ alpha, np.sqrt(np.maximum(np.diag(cov), 0))
