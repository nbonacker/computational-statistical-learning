# Setup
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

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

samples = np.random.multivariate_normal(np.zeros(len(X)), K, size=5)

plt.figure(figsize=(6,4))
for s in samples:
    plt.plot(X, s)
plt.title('GP Prior Samples')
plt.tight_layout()
plt.savefig(FIGURES / 'prior.png')
plt.close()

# Posterior
X_train = np.array([-0.9,-0.4,0.0,0.3,0.8])
y_train = np.sin(2*np.pi*X_train)

Ks = kernel(X_train, X)
K_train = kernel(X_train, X_train) + 0.05**2*np.eye(len(X_train))
Kss = kernel(X, X)

Kinv = np.linalg.inv(K_train)
mu = Ks.T @ Kinv @ y_train
cov = Kss - Ks.T @ Kinv @ Ks
std = np.sqrt(np.maximum(np.diag(cov), 0))

plt.figure(figsize=(6,4))
plt.plot(X, mu, label='Posterior Mean')
plt.fill_between(X, mu-2*std, mu+2*std, alpha=0.2)
plt.scatter(X_train, y_train)
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / 'posterior.png')
