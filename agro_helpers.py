"""Visual and statistical helpers for the susceptible-variety teaching lab.

The public notebook keeps student-facing cells short.  This module contains
the reproducible implementation and deliberately avoids private Statsmodels
attributes so that it remains compatible with current Colab runtimes.
"""

from __future__ import annotations

from io import BytesIO
from itertools import permutations, product
from pathlib import Path
from time import sleep
from urllib.request import urlopen
import platform
import re

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf

from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.patches import Polygon
from PIL import Image
from IPython.display import display
from scipy.stats import binomtest
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestPower


ORDER = ["Control", "Fungicide", "Inoculated"]
COLORS = {"Control": "#6B7280", "Fungicide": "#0072B2", "Inoculated": "#D55E00"}
MARKERS = {"Control": "o", "Fungicide": "s", "Inoculated": "^"}


def _download(url: str, attempts: int = 3, timeout: int = 25) -> bytes:
    """Download with a finite timeout and short retry loop."""
    last_error = None
    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=timeout) as response:
                return response.read()
        except Exception as error:  # network errors differ by runtime
            last_error = error
            if attempt + 1 < attempts:
                sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Could not download {url}") from last_error


def _points(wkt_text: str) -> np.ndarray:
    numbers = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", wkt_text)]
    return np.asarray(list(zip(numbers[0::2], numbers[1::2])))


class EvidenceLab:
    """Self-contained teaching interface; every activity can run independently."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.root = next((p for p in [Path("."), Path("..")] if (p / "data").exists()), None)
        self.field = self._table("field_plots.csv")
        self.events = self._table("field_events.csv")
        self.cnn = self._table("cnn_model_outputs.csv")
        self.rgb_early = self._picture("rgb_early_512.jpg")
        self.rgb_late = self._picture("rgb_late_512.jpg")
        self.field["treatment"] = pd.Categorical(self.field.treatment, ORDER, ordered=True)
        self.field["block"] = pd.Categorical(self.field.block)
        self.events["date"] = pd.to_datetime(self.events.date)
        self._mystery = (
            self.field[self.field.block.astype(int).eq(1)]
            .sample(frac=1, random_state=7)
            .reset_index(drop=True)
        )

    def _table(self, name: str) -> pd.DataFrame:
        if self.root:
            return pd.read_csv(self.root / "data" / name)
        payload = _download(f"{self.base_url}/data/{name}")
        return pd.read_csv(BytesIO(payload))

    def _picture(self, name: str) -> np.ndarray:
        if self.root:
            return np.asarray(Image.open(self.root / "assets" / name).convert("RGB"))
        payload = _download(f"{self.base_url}/assets/{name}")
        return np.asarray(Image.open(BytesIO(payload)).convert("RGB"))

    def versions(self) -> None:
        print(
            f"Ready · Python {platform.python_version()} · pandas {pd.__version__} · "
            f"statsmodels {statsmodels.__version__} · scikit-learn {sklearn.__version__}"
        )
        print(
            f"Data: {len(self.field)} field plots · {self.field.block.nunique()} blocks · "
            f"{self.field.treatment.nunique()} treatments · {len(self.cnn)} CNN rows"
        )

    def _crop(self, image: np.ndarray, polygon: str, pad: int = 3) -> np.ndarray:
        points = _points(polygon)
        x0, y0 = np.floor(points.min(axis=0) - pad).astype(int)
        x1, y1 = np.ceil(points.max(axis=0) + pad).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, image.shape[1]), min(y1, image.shape[0])
        return image[y0:y1, x0:x1]

    def _field_limits(self, polygon_column: str) -> tuple[float, float, float, float]:
        points = np.vstack([_points(value) for value in self.field[polygon_column]])
        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)
        return max(0, xmin - 12), min(512, xmax + 12), max(0, ymin - 22), min(512, ymax + 22)

    def _rgb_axis(self, ax, image: np.ndarray, polygon_column: str, title: str = "") -> None:
        xmin, xmax, ymin, ymax = self._field_limits(polygon_column)
        ax.imshow(image, origin="upper", extent=(0, 512, 512, 0), interpolation="nearest")
        ax.set(xlim=(xmin, xmax), ylim=(ymax, ymin), xticks=[], yticks=[], title=title)
        ax.set_aspect("equal")

    def _model(self, data: pd.DataFrame | None = None):
        source = self.field if data is None else data
        return smf.ols("sugar_content_pct ~ C(treatment) + C(block)", data=source).fit()

    @staticmethod
    def _contrast_rows(model, include_third: bool = True) -> pd.DataFrame:
        names = list(model.params.index)
        index = {name: position for position, name in enumerate(names)}
        fungicide = "C(treatment)[T.Fungicide]"
        inoculated = "C(treatment)[T.Inoculated]"
        definitions = [
            ("Fungicide − Control", {fungicide: 1.0}),
            ("Inoculated − Control", {inoculated: 1.0}),
        ]
        if include_third:
            definitions.append(("Fungicide − Inoculated", {fungicide: 1.0, inoculated: -1.0}))
        rows = []
        for label, weights in definitions:
            vector = np.zeros(len(names))
            for term, weight in weights.items():
                vector[index[term]] = weight
            result = model.t_test(vector)
            interval = np.asarray(result.conf_int())[0]
            rows.append(
                {
                    "contrast": label,
                    "difference": float(np.asarray(result.effect).item()),
                    "low": float(interval[0]),
                    "high": float(interval[1]),
                    "p_raw": float(np.asarray(result.pvalue).item()),
                }
            )
        table = pd.DataFrame(rows)
        table["p_holm"] = multipletests(table.p_raw, method="holm")[1]
        return table

    # ------------------------------------------------------------------
    # Field and image activities
    # ------------------------------------------------------------------
    def opening_field(self) -> None:
        fig, ax = plt.subplots(figsize=(11, 4.4))
        self._rgb_axis(
            ax,
            self.rgb_late,
            "polygon_late_px",
            "FIRST LOOK · September RGB orthomosaic · no labels yet",
        )
        plt.tight_layout()
        plt.show()

    def mystery_plots(self) -> None:
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.3))
        for label, ax, row in zip("ABC", axes, self._mystery.itertuples()):
            ax.imshow(self._crop(self.rgb_late, row.polygon_late_px), interpolation="nearest")
            ax.set_title(f"Mystery plot {label}", fontsize=13)
            ax.axis("off")
        fig.suptitle("TREATMENT DETECTIVE · September RGB crops", fontsize=18, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()

    def reveal_treatments(self, guesses: dict[str, str] | None = None) -> pd.DataFrame:
        rows = []
        for label, row in zip("ABC", self._mystery.itertuples()):
            guess = None if guesses is None else guesses.get(label)
            rows.append(
                {
                    "mystery plot": label,
                    "your guess": guess or "—",
                    "treatment": str(row.treatment),
                    "severity": row.severity_sep04,
                    "sugar content (%)": row.sugar_content_pct,
                    "correct?": "✓" if guess == str(row.treatment) else ("—" if guess is None else "✗"),
                }
            )
        result = pd.DataFrame(rows)
        display(result.style.hide(axis="index"))
        return result

    def image_to_number(self, plot_id: str = "P03", date: str = "September") -> float:
        row = self.field.loc[self.field.plot_id.eq(plot_id)].iloc[0]
        early = date.lower().startswith("j")
        image = self.rgb_early if early else self.rgb_late
        polygon = row.polygon_early_px if early else row.polygon_late_px
        released = row.early_green_share if early else row.late_green_share
        crop = self._crop(image, polygon).astype(float) / 255.0
        channel_sum = crop.sum(axis=2) + 1e-9
        red, green, blue = [crop[:, :, idx] / channel_sum for idx in range(3)]
        exg = 2 * green - red - blue
        mean_exg = float(exg.mean())
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.1))
        axes[0].imshow(crop)
        axes[0].set_title(f"{plot_id} · {date} RGB")
        heat = axes[1].imshow(exg, cmap="BrBG", vmin=-max(abs(exg.min()), abs(exg.max())),
                              vmax=max(abs(exg.min()), abs(exg.max())))
        axes[1].set_title("Excess-green (ExG) pixels")
        fig.colorbar(heat, ax=axes[1], shrink=.72)
        for ax in axes:
            ax.axis("off")
        fig.suptitle("IMAGE → NUMBER", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()
        print(f"Mean ExG reconstructed from the display JPEG: {mean_exg:.3f}")
        print(f"Released green-share descriptor:                 {released:.3f}")
        print("They are related descriptors, not identical pipelines; the JPEG is display-stretched.")
        return mean_exg

    def evidence_maps(self) -> None:
        specifications = [
            ("late_green_share", "Green share\ncontinuous descriptor", "YlGn"),
            ("severity_sep04", "Disease severity\nordered score", "OrRd"),
            ("sugar_content_pct", "Sugar content\ncontinuous outcome", "viridis"),
        ]
        fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.1))
        for ax, (column, title, cmap) in zip(axes, specifications):
            self._rgb_axis(ax, self.rgb_late, "polygon_late_px", title)
            ax.images[0].set_alpha(.18)
            patches = [Polygon(_points(text), closed=True) for text in self.field.polygon_late_px]
            values = self.field[column].to_numpy(float)
            collection = PatchCollection(
                patches, cmap=cmap, norm=Normalize(values.min(), values.max()),
                edgecolor="white", linewidth=1.3, alpha=.9,
            )
            collection.set_array(values)
            ax.add_collection(collection)
            for row in self.field.itertuples():
                center = _points(row.polygon_late_px)[:-1].mean(axis=0)
                ax.text(*center, row.plot_id, ha="center", va="center", fontsize=7, weight="bold")
            fig.colorbar(collection, ax=ax, shrink=.66, pad=.02)
        fig.suptitle("SAME FIELD · three variables, three statistical roles", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .89))
        plt.show()

    # ------------------------------------------------------------------
    # Design and inference activities
    # ------------------------------------------------------------------
    def pseudoreplication(self, copies: int = 50) -> pd.DataFrame:
        copies = max(1, int(copies))
        honest = self._contrast_rows(self._model(), include_third=False)
        copied = pd.concat([self.field] * copies, ignore_index=True)
        naive = self._contrast_rows(self._model(copied), include_third=False)
        honest["analysis"] = f"12 experimental plots"
        naive["analysis"] = f"same rows copied ×{copies}"
        combined = pd.concat([honest, naive], ignore_index=True)
        fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharex=False)
        for ax, contrast in zip(axes, honest.contrast):
            subset = combined[combined.contrast.eq(contrast)].reset_index(drop=True)
            y = np.arange(len(subset))[::-1]
            ax.axvline(0, color=".4", ls="--")
            ax.errorbar(
                subset.difference, y,
                xerr=[subset.difference - subset.low, subset.high - subset.difference],
                fmt="o", color="#0072B2", capsize=5, ms=8,
            )
            ax.set(yticks=y, yticklabels=subset.analysis, xlabel="Difference (percentage points)", title=contrast)
        fig.suptitle("PSEUDOREPLICATION TRAP · copied rows create fake precision", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()
        print("The estimate stays the same; the naive interval shrinks because copies were falsely treated as new experiments.")
        return combined

    def timeline(self) -> None:
        chosen = ["E01", "E02", "E03", "E04", "E08", "E09", "E10"]
        data = self.events[self.events.event_id.isin(chosen)].sort_values("days_after_sowing").copy()
        clusters = []
        current = []
        for row in data.itertuples():
            if current and row.days_after_sowing - current[-1].days_after_sowing > 3:
                clusters.append(current)
                current = []
            current.append(row)
        if current:
            clusters.append(current)

        palette = {"image": "#0072B2", "fungicide": "#009E73", "disease": "#D55E00"}
        fig, ax = plt.subplots(figsize=(12, 3.7))
        ax.hlines(0, data.days_after_sowing.min(), data.days_after_sowing.max(), color=".65", lw=3)
        cluster_number = 0
        for cluster in clusters:
            offsets = np.linspace(-11, 11, len(cluster)) if len(cluster) > 1 else np.array([0.0])
            levels = np.linspace(-.58, .58, len(cluster)) if len(cluster) > 1 else np.array([.38 if cluster_number % 2 == 0 else -.38])
            cluster_number += 1
            for row, offset, level in zip(cluster, offsets, levels):
                color = palette.get(row.event_type, "#7A5C1E")
                ax.scatter(row.days_after_sowing, 0, s=120, color=color, zorder=3)
                label = re.sub(r" \+ ", "\n+ ", row.event_label)
                ax.annotate(
                    f"{label}\nDAS {row.days_after_sowing}",
                    xy=(row.days_after_sowing, 0), xytext=(row.days_after_sowing + offset, level),
                    ha="center", va="bottom" if level > 0 else "top", fontsize=8.2,
                    arrowprops=dict(arrowstyle="-", color=color, lw=1.2),
                )
        same_day = data.groupby("days_after_sowing").size()
        for day in same_day[same_day.gt(1)].index:
            ax.axvspan(day - 1.2, day + 1.2, color="#FFD166", alpha=.28)
            ax.text(day, .79, "SAME DAY", ha="center", weight="bold", color="#8A5C00")
        ax.set(xlim=(data.days_after_sowing.min() - 5, data.days_after_sowing.max() + 5),
               ylim=(-.9, .9), xlabel="Days after sowing", yticks=[])
        sns.despine(ax=ax, left=True)
        ax.set_title("TIMING CHANGES THE QUESTION", fontsize=17, weight="bold")
        plt.tight_layout()
        plt.show()

    def randomization_test(self) -> tuple[float, float]:
        arranged = (
            self.field.assign(treatment=self.field.treatment.astype(str), block=self.field.block.astype(int))
            .sort_values(["block", "treatment"])
        )
        values = np.vstack([
            group.set_index("treatment").loc[ORDER, "sugar_content_pct"].to_numpy()
            for _, group in arranged.groupby("block", sort=True)
        ])
        observed = abs(values[:, 2].mean() - values[:, 0].mean())
        statistics = []
        all_permutations = list(permutations(range(3)))
        for assignment in product(all_permutations, repeat=values.shape[0]):
            permuted = np.vstack([values[block, perm] for block, perm in enumerate(assignment)])
            statistics.append(abs(permuted[:, 2].mean() - permuted[:, 0].mean()))
        statistics = np.asarray(statistics)
        p_exact = float(np.mean(statistics >= observed - 1e-12))
        fig, ax = plt.subplots(figsize=(9, 4.1))
        ax.hist(statistics, bins=28, color="#9ECAE1", edgecolor="white")
        ax.axvline(observed, color="#D55E00", lw=3, label=f"observed = {observed:.3f} pp")
        ax.set(xlabel="|Inoculated − Control| after reshuffling labels within blocks",
               ylabel="Number of random assignments",
               title=f"RANDOMIZATION TEST · {len(statistics):,} assignments · exact p = {p_exact:.4f}")
        ax.legend(frameon=False)
        sns.despine(ax=ax)
        plt.tight_layout()
        plt.show()
        return observed, p_exact

    def analyze_field(self, fungicide_guess: str | None = None, inoculated_guess: str | None = None) -> pd.DataFrame:
        model = self._model()
        contrasts = self._contrast_rows(model, include_third=True)
        treatment_p = float(anova_lm(model, typ=2).loc["C(treatment)", "PR(>F)"])
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), gridspec_kw={"width_ratios": [1, 1.25, 1.05]})

        for treatment in ORDER:
            group = self.field[self.field.treatment.eq(treatment)]
            x = ORDER.index(treatment)
            axes[0].scatter(
                np.full(len(group), x), group.sugar_content_pct,
                marker=MARKERS[treatment], s=72, color=COLORS[treatment], label=treatment, alpha=.9,
            )
        means = self.field.groupby("treatment", observed=True).sugar_content_pct.mean().reindex(ORDER)
        axes[0].plot(range(3), means, "_", color="black", ms=24, mew=3)
        axes[0].set(xticks=range(3), xticklabels=ORDER, ylabel="Sugar content (%)", title="Plots + treatment means")
        axes[0].tick_params(axis="x", rotation=18)

        y = np.arange(len(contrasts))[::-1]
        axes[1].axvline(0, color=".4", ls="--")
        axes[1].errorbar(
            contrasts.difference, y,
            xerr=[contrasts.difference - contrasts.low, contrasts.high - contrasts.difference],
            fmt="none", ecolor="#333333", capsize=5,
        )
        for position, row in zip(y, contrasts.itertuples()):
            marker = "s" if "Fungicide" in row.contrast.split(" − ")[0] else "^"
            axes[1].scatter(row.difference, position, marker=marker, s=70, color="#0072B2")
            axes[1].text(row.high + .06, position, f"Holm p={row.p_holm:.3g}", va="center", fontsize=8.5)
        span = max(abs(contrasts.low.min()), abs(contrasts.high.max()))
        axes[1].set_xlim(-span * 1.18, span * 1.35)
        axes[1].set(yticks=y, yticklabels=contrasts.contrast,
                    xlabel="Difference in sugar (percentage points)",
                    title="All three pairwise contrasts")

        for treatment in ORDER:
            group = self.field[self.field.treatment.eq(treatment)].sort_values("block")
            axes[2].plot(
                group.block.astype(int), group.sugar_content_pct,
                marker=MARKERS[treatment], color=COLORS[treatment], label=treatment, lw=2,
            )
        axes[2].set(xticks=sorted(self.field.block.astype(int).unique()), xlabel="Field block",
                    ylabel="Sugar content (%)", title="Pattern across blocks")
        axes[2].legend(frameon=False, fontsize=8)
        fig.suptitle("BLOCKED ANALYSIS · estimates before significance labels", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .9))
        plt.show()

        print(f"Global treatment test: p = {treatment_p:.3g}")
        actual = {
            "Fungicide": "higher" if contrasts.iloc[0].difference > 0 else "lower",
            "Inoculated": "higher" if contrasts.iloc[1].difference > 0 else "lower",
        }
        if fungicide_guess:
            print(f"Your Fungicide prediction: {fungicide_guess} · observed: {actual['Fungicide']}")
        if inoculated_guess:
            print(f"Your Inoculated prediction: {inoculated_guess} · observed: {actual['Inoculated']}")
        return contrasts

    def ancova_sensitivity(self) -> pd.DataFrame:
        data = self.field.assign(
            green_c=self.field.early_green_share - self.field.early_green_share.mean()
        )
        primary = self._model()
        ancova = smf.ols(
            "sugar_content_pct ~ C(treatment) + C(block) + green_c", data=data
        ).fit()
        green_ci = ancova.conf_int().loc["green_c"]
        table = pd.DataFrame(
            [
                {
                    "analysis": "Primary: treatment + block",
                    "treatment p": anova_lm(primary, typ=2).loc["C(treatment)", "PR(>F)"],
                    "June-green coefficient": np.nan,
                    "green CI low": np.nan,
                    "green CI high": np.nan,
                    "residual df": primary.df_resid,
                },
                {
                    "analysis": "Sensitivity: + June green",
                    "treatment p": anova_lm(ancova, typ=2).loc["C(treatment)", "PR(>F)"],
                    "June-green coefficient": ancova.params["green_c"],
                    "green CI low": green_ci.iloc[0],
                    "green CI high": green_ci.iloc[1],
                    "residual df": ancova.df_resid,
                },
            ]
        )
        display(table.round(3).style.hide(axis="index"))
        print(
            "June green is post-treatment/same-day ambiguous, so this is a conditional sensitivity analysis—not a repaired baseline."
        )
        return table

    def drop_one_plot(self, plot_id: str) -> pd.DataFrame:
        full = self._contrast_rows(self._model(), include_third=False)
        reduced_data = self.field.loc[~self.field.plot_id.eq(plot_id)].copy()
        reduced = self._contrast_rows(self._model(reduced_data), include_third=False)
        full["analysis"] = "all plots"
        reduced["analysis"] = f"without {plot_id}"
        combined = pd.concat([full, reduced], ignore_index=True)
        fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
        for ax, contrast in zip(axes, full.contrast):
            subset = combined[combined.contrast.eq(contrast)].reset_index(drop=True)
            y = np.arange(len(subset))[::-1]
            ax.axvline(0, color=".4", ls="--")
            for position, row, color, marker in zip(y, subset.itertuples(), ["#6B7280", "#0072B2"], ["o", "s"]):
                ax.errorbar(row.difference, position,
                            xerr=[[row.difference - row.low], [row.high - row.difference]],
                            fmt=marker, color=color, capsize=5, ms=7)
            ax.set(yticks=y, yticklabels=subset.analysis, xlabel="Difference (percentage points)", title=contrast)
        fig.suptitle("REMOVE ONE PLOT · sensitivity, not permission to delete", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()
        return combined

    def correlation_trap(self) -> tuple[float, float]:
        x = self.field.late_green_share.to_numpy()
        y = self.field.sugar_content_pct.to_numpy()
        overall = float(np.corrcoef(x, y)[0, 1])
        x_centered = self.field.late_green_share - self.field.groupby("treatment", observed=True).late_green_share.transform("mean")
        y_centered = self.field.sugar_content_pct - self.field.groupby("treatment", observed=True).sugar_content_pct.transform("mean")
        within = float(np.corrcoef(x_centered, y_centered)[0, 1])
        fig, axes = plt.subplots(1, 2, figsize=(10.5, 4))
        sns.regplot(data=self.field, x="late_green_share", y="sugar_content_pct", ax=axes[0],
                    scatter=False, color="#333333")
        for treatment in ORDER:
            group = self.field[self.field.treatment.eq(treatment)]
            axes[0].scatter(group.late_green_share, group.sugar_content_pct,
                            color=COLORS[treatment], marker=MARKERS[treatment], s=72, label=treatment)
            sns.regplot(data=group, x="late_green_share", y="sugar_content_pct", ax=axes[1],
                        scatter=False, ci=None, color=COLORS[treatment])
            axes[1].scatter(group.late_green_share, group.sugar_content_pct,
                            color=COLORS[treatment], marker=MARKERS[treatment], s=72)
        axes[0].set_title(f"All plots together · r = {overall:.2f}")
        axes[0].legend(frameon=False, fontsize=8)
        axes[1].set_title(f"Within-treatment association · r = {within:.2f}")
        fig.suptitle("CORRELATION TRAP · groups can create the pattern", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()
        return overall, within

    def model_health(self) -> list[str]:
        model = self._model()
        cooks = model.get_influence().cooks_distance[0]
        guide = 4 / len(self.field)
        influential = self.field.loc[cooks > guide, "plot_id"].tolist()
        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        axes[0].scatter(model.fittedvalues, model.resid, color="#0072B2", s=58)
        axes[0].axhline(0, color=".4", ls="--")
        axes[0].set(xlabel="Fitted", ylabel="Residual", title="Pattern?")
        sm.qqplot(model.resid, line="45", fit=True, ax=axes[1])
        axes[1].set_title("Strong outlier?")
        axes[2].stem(np.arange(1, len(self.field) + 1), cooks, basefmt=" ")
        axes[2].axhline(guide, color="#D55E00", ls="--", label="4/n guide")
        for index, value in enumerate(cooks):
            if value > guide:
                axes[2].text(index + 1, value + .015, self.field.iloc[index].plot_id,
                             ha="center", fontsize=8, weight="bold")
        axes[2].set(xlabel="Plot number", ylabel="Cook's distance", title="Influential plot?")
        axes[2].legend(frameon=False, fontsize=8)
        fig.suptitle("MODEL HEALTH · inspect; never delete automatically", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .9))
        plt.show()
        print("Plots above the 4/n guide:", ", ".join(influential) if influential else "none")
        return influential

    def residual_map(self) -> None:
        model = self._model()
        residuals = pd.Series(np.asarray(model.resid), index=self.field.plot_id)
        values = self.field.plot_id.map(residuals).to_numpy()
        limit = max(abs(values.min()), abs(values.max()))
        fig, ax = plt.subplots(figsize=(8, 4.4))
        self._rgb_axis(ax, self.rgb_late, "polygon_late_px", "SPATIAL CHECK · residuals in preview-pixel space")
        ax.images[0].set_alpha(.2)
        patches = [Polygon(_points(text), closed=True) for text in self.field.polygon_late_px]
        collection = PatchCollection(
            patches, cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0, vmin=-limit, vmax=limit),
            edgecolor="white", linewidth=1.4, alpha=.9,
        )
        collection.set_array(values)
        ax.add_collection(collection)
        for row in self.field.itertuples():
            center = _points(row.polygon_late_px)[:-1].mean(axis=0)
            ax.text(*center, row.plot_id, ha="center", va="center", fontsize=8, weight="bold")
        fig.colorbar(collection, ax=ax, shrink=.72, label="Observed − fitted sugar (percentage points)")
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------------
    # Optional CNN and extension activities
    # ------------------------------------------------------------------
    def inspect_cnn_fold(self, fold: int = 1) -> None:
        fold = int(fold)
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        for ax, image, polygon, title in [
            (axes[0], self.rgb_early, "polygon_early_px", "June"),
            (axes[1], self.rgb_late, "polygon_late_px", "September"),
        ]:
            self._rgb_axis(ax, image, polygon, title)
            for row in self.field.itertuples():
                points = _points(getattr(row, polygon))
                selected = int(row.block) == fold
                ax.add_patch(Polygon(points, fill=False, edgecolor="#D55E00" if selected else "white",
                                     linewidth=3 if selected else .7))
        fig.suptitle(f"GROUPED SPLIT · Fold {fold} tests every plot from Block {fold}", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .9))
        plt.show()

    def leakage_demo(self) -> tuple[float, float]:
        # Deliberately cheating lookup model: it can memorize a plot when the
        # other date from the same plot appears in training.
        data = self.cnn.copy()
        features = data[["plot_id"]]
        target = data.true_class
        encoder = ColumnTransformer(
            [("plot fingerprint", OneHotEncoder(handle_unknown="ignore"), ["plot_id"])]
        )
        estimator = make_pipeline(
            encoder,
            LogisticRegression(C=1000, max_iter=1000),
        )
        random_cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=12)
        grouped_cv = GroupKFold(n_splits=self.field.block.nunique())
        random_prediction = cross_val_predict(estimator, features, target, cv=random_cv)
        grouped_prediction = cross_val_predict(
            estimator, features, target, groups=data.held_out_block, cv=grouped_cv
        )
        random_accuracy = accuracy_score(target, random_prediction)
        grouped_accuracy = accuracy_score(target, grouped_prediction)
        fig, ax = plt.subplots(figsize=(7.5, 3.8))
        ax.bar([0, 1], [random_accuracy, grouped_accuracy], color=["#D55E00", "#0072B2"], width=.58)
        ax.set(xticks=[0, 1], xticklabels=["Random image rows\n(leaky risk)", "Whole blocks\n(grouped)"],
               ylim=(0, 1.05), ylabel="Toy classifier accuracy",
               title="SPLIT CHANGES THE ANSWER")
        for position, value in enumerate([random_accuracy, grouped_accuracy]):
            ax.text(position, value + .04, f"{value:.0%}", ha="center", weight="bold")
        sns.despine(ax=ax)
        plt.tight_layout()
        plt.show()
        print("Toy model = a deliberately cheating plot-ID lookup; it is not the CNN.")
        print("Random rows reward memorization because the other date from the same plot can be in training.")
        print("Whole-block splitting removes every fingerprint from the held-out block.")
        return random_accuracy, grouped_accuracy

    def evaluate_cnn(self) -> pd.DataFrame:
        data = self.cnn.copy()
        data["correct"] = data.true_class.eq(data.cnn_prediction)
        groups = list(data.groupby("date", sort=True))
        summary = []
        fig = plt.figure(figsize=(13, 5))
        grid = fig.add_gridspec(1, 3, width_ratios=[.8, 1, 1])
        ax0 = fig.add_subplot(grid[0, 0])
        counts = []
        for date, group in groups:
            correct = int(group.correct.sum())
            p_value = float(binomtest(correct, len(group), 1 / len(ORDER), alternative="greater").pvalue)
            counts.append(correct)
            summary.append({"date": date, "correct": correct, "n": len(group), "accuracy": correct / len(group),
                            "exact p vs 1/3": p_value})
        ax0.bar(range(len(groups)), counts, color=["#9ECAE1", "#0072B2"], width=.6)
        for position, (correct, (_, group)) in enumerate(zip(counts, groups)):
            ax0.text(position, correct + .25, f"{correct}/{len(group)}", ha="center", weight="bold", fontsize=13)
        ax0.set(xticks=range(len(groups)), xticklabels=[pd.Timestamp(date).strftime("%d %b") for date, _ in groups],
                ylim=(0, max(len(group) for _, group in groups) + 1), ylabel="Correct predictions",
                title="Observed CNN counts")
        for ax, (date, group) in zip([fig.add_subplot(grid[0, 1]), fig.add_subplot(grid[0, 2])], groups):
            ConfusionMatrixDisplay.from_predictions(
                group.true_class, group.cnn_prediction, labels=ORDER,
                display_labels=["Ctrl", "Fung.", "Inoc."], cmap="Blues", colorbar=False, ax=ax,
            )
            ax.set_title(pd.Timestamp(date).strftime("%d %B"))
            ax.set_xlabel("CNN prediction")
        fig.suptitle("CNN EVIDENCE · inspect classes, not only total accuracy", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .9))
        plt.show()
        summary = pd.DataFrame(summary)
        display(summary.round(3).style.hide(axis="index"))
        return summary

    def producer_view(self) -> pd.DataFrame:
        data = self.field.copy()
        data["sugar_mass_per_sample_kg"] = data.root_weight * data.sugar_content_pct / 100
        summary = (
            data.groupby("treatment", observed=True)[["root_weight", "sugar_content_pct", "sugar_mass_per_sample_kg"]]
            .mean().reindex(ORDER)
        )
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
        for ax, column, title in zip(
            axes,
            ["root_weight", "sugar_content_pct", "sugar_mass_per_sample_kg"],
            ["Root weight (kg/sample)", "Sugar content (%)", "Sugar mass (kg/sample)"],
        ):
            for treatment in ORDER:
                group = data[data.treatment.eq(treatment)]
                ax.scatter(np.full(len(group), ORDER.index(treatment)), group[column],
                           color=COLORS[treatment], marker=MARKERS[treatment], s=65)
            ax.set(xticks=range(3), xticklabels=ORDER, title=title)
            ax.tick_params(axis="x", rotation=18)
        fig.suptitle("PRODUCER VIEW · content is not yield and neither is profit", fontsize=17, weight="bold")
        plt.tight_layout(rect=(0, 0, 1, .88))
        plt.show()
        print("This is sugar mass per source sample—not field yield or profit. Area, price and fungicide cost are still missing.")
        return summary

    def power_sandbox(self, blocks: int = 4, target_difference: float = 0.30) -> float:
        model = self._model()
        residual_sd = float(np.sqrt(model.mse_resid))
        paired_sd_approx = np.sqrt(2) * residual_sd
        effect_size = float(target_difference) / paired_sd_approx
        power = float(TTestPower().power(effect_size=effect_size, nobs=max(2, int(blocks)), alpha=.05))
        block_grid = np.arange(3, 13)
        powers = [TTestPower().power(effect_size=effect_size, nobs=int(number), alpha=.05) for number in block_grid]
        fig, ax = plt.subplots(figsize=(7.5, 3.8))
        ax.plot(block_grid, powers, marker="o", color="#0072B2")
        ax.scatter([blocks], [power], marker="s", s=90, color="#D55E00", zorder=3)
        ax.axhline(.8, color=".45", ls="--", label="80% reference")
        ax.set(xticks=block_grid, ylim=(0, 1.03), xlabel="Blocks", ylabel="Approximate power",
               title=f"DESIGN SANDBOX · target difference = {target_difference:.2f} pp")
        ax.legend(frameon=False)
        sns.despine(ax=ax)
        plt.tight_layout()
        plt.show()
        print("Planning approximation only: it reuses the residual variation from this small completed trial.")
        return power

    @staticmethod
    def score_quiz(answers: dict[str, str], pre_answers: dict[str, str] | None = None) -> int:
        key = {
            "unit": "field plot",
            "baseline": "no",
            "pvalue": "data compatibility under the null model",
            "cnn_split": "whole field block",
            "correlation": "no",
        }
        score = sum(str(answers.get(question, "")).lower() == expected for question, expected in key.items())
        print(f"Score: {score}/{len(key)}")
        if pre_answers is not None:
            pre_score = sum(str(pre_answers.get(question, "")).lower() == expected for question, expected in key.items())
            print(f"Pre-course score: {pre_score}/{len(key)} · change: {score - pre_score:+d}")
        return score
