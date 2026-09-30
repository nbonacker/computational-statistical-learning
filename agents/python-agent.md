# Python Agent

## Purpose

Build intuition for statistical learning through small, reproducible Python examples.

## Dependencies

Preferably use the following packages:

- numpy
- scipy
- matplotlib

Suggest using additional packages only when they clearly improve the example.

## Coding Style

- Favor clarity over performance.
- Favor intuition over completeness.
- Keep scripts small and easy to read.
- Use descriptive variable names.
- Minimal comments.
- Prefer explicit implementations over framework abstractions.
- Use fixed random seed 0 for reproducibility.
- Implement algorithms from first principles whenever practical.

## Visualization Style

Default:

```python
plt.style.use("bmh")
```

General:

- readable axis labels
- concise titles
- consistent figure sizes
- `constrained_layout=True`
- legends only when needed

### Scatter Plots

```python
ax.scatter(
    x,
    y,
    s=20,
    alpha=0.7,
    edgecolors="none",
)
```

Grouped data:

```python
ax.scatter(
    x,
    y,
    c=group,
    cmap="viridis",
    s=20,
    alpha=0.7,
)
```

### Histograms

```python
ax.hist(
    x,
    bins=50,
    density=True,
    alpha=0.7,
)
```

Overlay analytical distributions whenever possible.

### Multi-Panel Figures

```python
fig, axs = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(10, 8),
    constrained_layout=True,
)
```

## Statistical Learning Principles

- Start with synthetic data.
- Visualize assumptions.
- Compare against ground truth.
- Prefer understanding over optimization.

## Deliverables

Each topic should contain:

- runnable implementation
- generated figures
- concise README
- key takeaways

## Goal

Create a collection of minimal examples that develop intuition for statistical learning algorithms and probabilistic modeling through implementation and visualization.
