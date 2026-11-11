# Setup
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from gaussian_process import kernel, posterior
plt.style.use('bmh')

rng = np.random.default_rng(42)

FIGURES = Path(__file__).parent / 'figures'
FIGURES.mkdir(exist_ok=True)


# Prior
X = np.linspace(-1, 1, 100)
K = kernel(X, X) + 1e-8 * np.eye(len(X))

samples = rng.multivariate_normal(np.zeros(len(X)), K, size=5)

fig, ax = plt.subplots(1, 1, figsize=(6,3))
for i, s in enumerate(samples):
   ax.plot(X, s)
ax.set_title('Gaussian Process Prior', size=10)
ax.set_xlabel('X', size=10)
ax.set_ylabel('Y', size=10)
fig.tight_layout()
fig.savefig(FIGURES / 'prior.png')
plt.close()

# Posterior
X_train = np.array([-0.9,-0.4,0.0,0.3,0.8])
y_train = np.sin(2*np.pi*X_train)

mu, std = posterior(X_train, y_train, X)

fig, ax = plt.subplots(1, 1, figsize=(6,3))
ax.plot(X, mu, label='Posterior mean function')
ax.set_xlabel('X', size=10)
ax.set_ylabel('Y', size=10)
ax.set_title('Gaussian Process Posterior', size=10)
ax.fill_between(X, mu-2*std, mu+2*std, alpha=0.2, label='95% confidence interval')
ax.scatter(X_train, y_train, label='Training data')
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES / 'posterior.png')
plt.close()
