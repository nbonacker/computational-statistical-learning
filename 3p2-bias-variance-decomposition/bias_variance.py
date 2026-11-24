import numpy as np


def design_matrix(x, centers, s):
    """Bias column followed by one Gaussian basis function per center."""
    gaussians = np.exp(-0.5 * ((x[:, None] - centers) / s) ** 2)
    return np.column_stack([np.ones(len(x)), gaussians])


def fit_ridge(Phi, t, lambda_):
    """Regularized least squares, compare https://en.wikipedia.org/wiki/Regularized_least_squares"""
    return np.linalg.solve(lambda_ * np.eye(Phi.shape[1]) + Phi.T @ Phi, Phi.T @ t)
