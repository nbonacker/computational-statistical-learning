# Setup
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from bias_variance import design_matrix, fit_ridge
plt.style.use('bmh')

rng = np.random.default_rng(42)

FIGURES = Path(__file__).parent / 'figures'
FIGURES.mkdir(exist_ok=True)

L = 100                            # number of data sets
N = 25                             # points per data set
N_TEST = 1000                      # points in the test set
NOISE = 0.3                        # standard deviation of the target noise
CENTERS = np.linspace(0, 1, 24)    # Gaussian basis function centers
WIDTH = 0.05                       # Gaussian basis function width s
LN_LAMBDAS = np.linspace(-3, 2, 30)
LN_LAMBDAS_FITS = [2.6, -0.31, -2.4]


def h(x):
    return np.sin(2 * np.pi * x)


X = np.linspace(0, 1, 100)
Phi_X = design_matrix(X, CENTERS, WIDTH)

x_train = rng.uniform(0, 1, (L, N))
t_train = h(x_train) + rng.normal(0, NOISE, (L, N))
Phi_train = [design_matrix(x, CENTERS, WIDTH) for x in x_train]
x_test = rng.uniform(0, 1, N_TEST)
t_test = h(x_test) + rng.normal(0, NOISE, N_TEST)
Phi_test = design_matrix(x_test, CENTERS, WIDTH)


def fit_all(lambda_):
    """Weights of the model fitted to each of the L data sets, shape (L, M)."""
    return np.array([fit_ridge(Phi, t, lambda_) for Phi, t in zip(Phi_train, t_train)])


# Regularization strength (compare Bishop Fig. 3.5)
fig, axs = plt.subplots(3, 2, figsize=(6, 9), sharex=True, sharey=True)
for i, ln_lambda in enumerate(LN_LAMBDAS_FITS):
    y = fit_all(np.exp(ln_lambda)) @ Phi_X.T
    axs[i, 0].plot(X, y[:20].T, alpha=0.5, linewidth=1)
    axs[i, 1].plot(X, h(X), label='Ground truth')
    axs[i, 1].plot(X, y.mean(axis=0), label='Average fit')
    for j in range(2):
        axs[i, j].grid(True)
        axs[i, j].set_title(f'ln λ = {ln_lambda}', size=10)
    axs[i, 0].set_ylabel('t', size=10)
axs[0, 1].legend(fontsize=10)
axs[2, 0].set_xlabel('x', size=10)
axs[2, 1].set_xlabel('x', size=10)
fig.suptitle('Regularization', size=12)
fig.tight_layout()
fig.savefig(FIGURES / 'regularization.png')
plt.close(fig)

# Bias-variance decomposition (compare Bishop Fig. 3.6)
bias2, variance, test_error = [], [], []
for ln_lambda in LN_LAMBDAS:
    W = fit_all(np.exp(ln_lambda))
    y = W @ Phi_X.T
    y_mean = y.mean(axis=0)
    bias2.append(np.mean((y_mean - h(X)) ** 2))
    variance.append(np.mean((y - y_mean) ** 2))
    test_error.append(np.mean((W @ Phi_test.T - t_test) ** 2))
bias2, variance, test_error = np.array(bias2), np.array(variance), np.array(test_error)

fig, ax = plt.subplots(1, 1, figsize=(6, 3))
ax.plot(LN_LAMBDAS, bias2, label='(bias)²')
ax.plot(LN_LAMBDAS, variance, label='variance')
ax.plot(LN_LAMBDAS, bias2 + variance, label='(bias)² + variance')
ax.plot(LN_LAMBDAS, test_error, label='test error')
ax.grid(True)
ax.set_xlabel('ln λ', size=10)
ax.set_ylabel('Error', size=10)
ax.set_title('Bias-variance decomposition', size=12)
ax.legend(fontsize=10)
fig.tight_layout()
fig.savefig(FIGURES / 'bias_variance.png')
plt.close(fig)

print(f'Minimum of bias^2 + variance at ln lambda = {LN_LAMBDAS[np.argmin(bias2 + variance)]:.2f}')
print(f'Minimum of test error at ln lambda = {LN_LAMBDAS[np.argmin(test_error)]:.2f}')
