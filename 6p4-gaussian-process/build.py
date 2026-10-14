# Setup
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

FIGURES = Path(__file__).parent / 'figures'
FIGURES.mkdir(exist_ok=True)


# Kernel
def kernel(x1, x2, length_scale=0.4):
    x1 = np.atleast_2d(x1).T
    x2 = np.atleast_2d(x2).T
    return np.exp(-0.5 * ((x1 - x2.T) / length_scale) ** 2)


# Prior
X = np.linspace(-1, 1, 100)
K = kernel(X, X) + 1e-8 * np.eye(len(X))

samples = rng.multivariate_normal(np.zeros(len(X)), K, size=5)

plt.figure(figsize=(6,4))
for i, s in enumerate(samples):
   plt.plot(X, s)
plt.title('Gaussian Process Prior', size=12)
plt.xlabel('X', size=10)
plt.ylabel('Y', size=10)
plt.tight_layout()
plt.savefig(FIGURES / 'prior.png')
plt.close()

# Posterior
X_train = np.array([-0.9,-0.4,0.0,0.3,0.8])
y_train = np.sin(2*np.pi*X_train)

Ks = kernel(X_train, X)
K_train = kernel(X_train, X_train) + 0.05**2*np.eye(len(X_train))
Kss = kernel(X, X)

# Cholesky decomposition
L = np.linalg.cholesky(K_train)
alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_train))
mu = Ks.T @ alpha

v = np.linalg.solve(L, Ks)
cov = Kss - v.T @ v
std = np.sqrt(np.maximum(np.diag(cov), 0))

plt.figure(figsize=(6,4))
plt.plot(X, mu, label='Posterior mean function')
plt.xlabel('X', size=10)
plt.ylabel('Y', size=10)
plt.title('Gaussian Process Posterior', size=12)
plt.fill_between(X, mu-2*std, mu+2*std, alpha=0.2, label='95% confidence interval')
plt.scatter(X_train, y_train, label='Training data')
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / 'posterior.png')
plt.close()
