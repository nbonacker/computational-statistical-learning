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

Time series, shared y:

```python
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

Scatter x vs y comparison (e.g. two measurements per sensor), one condition per panel, with a grey identity line:

```python
def plot_predictions_vs_measurements(x: dict, y: dict, conditions: list, model: str, version: str, out_dir: Path) -> None:
    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    for ax, cond in zip(axs.flat, conditions):
        ax.scatter(x[cond], y[cond])
        lim = [min(x[cond].min(), y[cond].min()), max(x[cond].max(), y[cond].max())]
        ax.plot(lim, lim, color='grey', ls='--', zorder=0)
        ax.grid(True)
        ax.set_xlabel('Measurement [vol.%CO2]', size=10)
        ax.set_ylabel('Prediction [vol.%CO2]', size=10)
        ax.set_title(cond, size=10)
    fig.suptitle(f'{model} {version}', size=12)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_dir / f'<script>_{model}.png')
    plt.close(fig)
```

## Optional extras

- Reference lines: `color='grey', ls='--'`; zero lines, specifications or model fits: `color='darkred', ls='--'`.
- Legends only for multiple datasets: `fontsize=10`, default placement unless it obscures data.
- Wide-range concentrations: `ax.set_yscale('symlog', linthresh=10)`; set ticks once on the first axis after plotting (step 2 within ±10, 1-2-5 steps outside, filtered to `ax.get_ylim()`) with plain-number formatting (`from matplotlib.ticker import FuncFormatter`):

```python
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:g}'))
y_min, y_max = axs[0].get_ylim()
outer = np.array([m * 10 ** e for e in range(1, 5) for m in (1, 2, 5)])
ticks = np.unique(np.concatenate([np.arange(-10, 11, 2), outer, -outer]))
axs[0].set_yticks(ticks[(ticks >= y_min) & (ticks <= y_max)])
```
- Plots with applied FRC: add `with Frc` to the figure title and `_frc` to the file name.
