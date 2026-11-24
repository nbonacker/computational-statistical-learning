---
name: plotting
description: Conventions for creating Matplotlib plots. Use when adding or changing any plot.
---

# Plotting skill

Reference: `plot_pre_post` in `PythonScripts/shelf_live_time/shelf_live_time.py`.

## Rules

- Matplotlib only; `plt.style.use('bmh')` once at the top of the script, keep its grey background.
- Subplots for multiple axes; `sharex`/`sharey=True` for panels with the same quantity. Don't clip or limit axes unless asked.
- `ax.grid(True)` on every axis.
- Prefer scatter plots for data.
- Prefer default marker size and color.
- Subtitle and axis labels with `size=10`, figure title with `size=12`.
- Prefer `for ax in axs` for 1D subplot arrays and `axs[i, j]` for 2D grids (no `axs.flat`).
- Axis labels with units in brackets, `size=10`: `'Time [min]'`, `'Concentration [vol.%CO2]'`, `'Temperature [°C]'`, `'Pressure [mBar]'`, `'Relative humidity [%]'`. With `sharey=True`, set the y label on the first panel only.
- Subplot titles: short, `size=10` (`'Pre'`, `'Post'`, or fixed conditions like `'1000mBar, 20°C'`).
- Figure title: `fig.suptitle(f'Sbc41 gm{gm_idx} {version}', size=12)`.
- `figsize=(6, 3)` for 1x2 panels, scaled by panel count; `(8, 4)` for timetraces or multiple modes.
- Measurement data: `ax.scatter(x, y)` with default marker size and color. Time series: x = elapsed time in minutes, `(df.Epoch_UTC - df.Epoch_UTC.iloc[0]) / 60`.

## Output

- `FIGURES_DIR = Path(__file__).parent / "figures"`; `out_dir.mkdir(parents=True, exist_ok=True)`; use `Path` objects.
- `fig.tight_layout()`, then PNG only: `fig.savefig(out_dir / f'<script>_gm{gm_idx}.png')` (no dpi/facecolor); then `plt.close(fig)`.
- Descriptive file names with the gas-model index, one figure per gas model.

## Templates

Time series with shared y:

```python
import matplotlib.pyplot as plt
import pandas as pd

def plot_time_series(df_pre: pd.DataFrame, df_post: pd.DataFrame, gm_idx: str, version: str, out_dir: Path) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(6, 3), sharey=True)
    for ax, df, title in zip(axs, (df_pre, df_post), ('Pre', 'Post')):
        ax.scatter((df.Epoch_UTC - df.Epoch_UTC.iloc[0]) / 60, df[f'Conc_{gm_idx}'])
        ax.grid(True)
        ax.set_title(title, size=10)
        ax.set_xlabel('Time [min]', size=10)
    axs[0].set_ylabel('Concentration [vol.%CO2]', size=10)
    fig.suptitle(f'Sbc41 gm{gm_idx} {version}', size=12)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_dir / f'<script>_gm{gm_idx}.png')
    plt.close(fig)
```

Scatter x vs y (e.g. two measurements per sensor), with a grey identity line:

```python
import matplotlib.pyplot as plt

def plot_predictions_vs_measurements(x: dict, y: dict, conditions: list, model: str, version: str, out_dir: Path) -> None:
    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    for i in range(2):
        for j in range(2):
            cond = conditions[2 * i + j]
            axs[i, j].scatter(x[cond], y[cond])
            lim = [min(x[cond].min(), y[cond].min()), max(x[cond].max(), y[cond].max())]
            axs[i, j].plot(lim, lim, color='grey', ls='--', zorder=0)
            axs[i, j].grid(True)
            axs[i, j].set_xlabel('Measurement [vol.%CO2]', size=10)
            axs[i, j].set_ylabel('Prediction [vol.%CO2]', size=10)
            axs[i, j].set_title(cond, size=10)
    fig.suptitle(f'{model} {version}', size=12)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_dir / f'<script>_{model}.png')
    plt.close(fig)
```

## Optional extras

- Reference lines: `color='grey', ls='--'`; zero lines, specifications or model fits: `color='darkred', ls='--'`.
- Legends only for multiple datasets: `fontsize=10`, default placement unless it obscures data.
- Wide-range data: `ax.set_yscale('symlog', linthresh=10)`; set ticks once on the first axis after plotting (step 2 within ±10, 1-2-5 steps outside, filtered to `ax.get_ylim()`) with plain-number formatting (`from matplotlib.ticker import FuncFormatter`):