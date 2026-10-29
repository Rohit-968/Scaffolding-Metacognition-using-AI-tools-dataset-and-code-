# From Scaffolding to Dependency — Data Analysis Replication

Replication package for the survey study *From Scaffolding to Dependency? University Students' Perceptions of Generative AI in Metacognition and Academic Writing*.

Rohit Vinod (230968045) · Abhay Vineetha Anil (230962109) · Guide: Dr. Bharath Suresh Kumar
Department of Humanities and Management, MIT Manipal · October 2026

This repository lets a reviewer re-run every number in the *Data Analysis Summary* from the original survey export, and see exactly what was changed in the data and why.

## Repository contents

| Path | What it is |
| --- | --- |
| `data/raw/responses_csv.csv` | Original Google Forms export, **unchanged** (303 responses × 36 columns) |
| `data/processed/cleaned_data.csv` | Analysis dataset (286 responses): numeric item scores, consent flag, outlier flag, construct scores and the original row number for every respondent |
| `data/processed/changes_log.csv` | Every change made to the raw data: 17 rows removed (with reason), 15 blank answers imputed (with value), 25 outliers flagged but kept |
| `data/processed/codebook.csv` | Item codes (AI1–AW8) mapped to the full question wording |
| `analysis.py` | The complete analysis, from raw CSV to every reported statistic |
| `results/computed_values.csv` | Every statistic produced by `analysis.py` |
| `results/analysis_log.txt` | Console output of the run that produced the files above |
| `results/cfa_loadings.csv`, `results/efa_loadings.csv` | Factor loadings (final CFA model; 4-factor oblimin EFA) |
| `results/sem_bootstrap_draws.csv` | All 5,000 bootstrap estimates of the structural paths and indirect effects |
| `VERIFICATION_REPORT.md` | Line-by-line comparison of the Data Analysis Summary with the re-computed values |

## Raw data integrity

The raw file is byte-identical to the original export. SHA-256:

```
95dd89804fa708c67f7415fd1d43c4fcefae746ac7d4d2965c1c75fb2fb86a3b  data/raw/responses_csv.csv
```

Check with `sha256sum data/raw/responses_csv.csv` (Linux/macOS) or `Get-FileHash data\raw\responses_csv.csv` (Windows PowerShell).

## Changes made to the data

Responses were converted from text labels (e.g. `5 = Somewhat Agree`) to numbers (5) and columns were renamed to item codes (see `codebook.csv`). Then, in this order:

| Step | Rule | Removed | Remaining |
| --- | --- | --- | --- |
| Raw export | — | — | 303 |
| Duplicates | Identical answers on all 34 items | 6 | 297 |
| Incomplete | More than 3 of 34 items blank | 5 | 292 |
| Straight-lining | Same answer on every item | 6 | 286 |

The 15 remaining blank answers (0.15% of all answers) were filled with the item median. 25 multivariate outliers (Mahalanobis D², p < .001) were kept in the main analysis and removed only in a robustness check. Every affected respondent is listed by original row number in `changes_log.csv`.

## How to run

Python 3.12 was used.

```
pip install -r requirements.txt
python analysis.py
```

Run from the repository root. A full run takes about 10–15 minutes because of the 5,000 SEM bootstrap resamples (set `N_BOOT` at the top of `analysis.py` to a small number for a quick check; all other values are unaffected). The run overwrites the files in `data/processed/` and `results/`.

`factor_analyzer` 0.5.1 calls a scikit-learn argument that was renamed in scikit-learn 1.6; the first lines of `analysis.py` bridge this so the script works with current scikit-learn.

## Analysis steps

| Summary section | Method |
| --- | --- |
| 1 Cleaning, normality | Rules above; item skewness/kurtosis; Mardia's multivariate kurtosis |
| 2 Descriptives | Construct means, SD, 95% CI, % agree (mean ≥ 5), one-sample t-test vs 4, Cohen's d |
| 3 Reliability | Cronbach's α, McDonald's ω (from CFA loadings), corrected item–total correlations |
| 4 Factor structure | KMO, Bartlett, parallel analysis (1,000 random datasets), 4-factor oblimin EFA, CFA models M0–M4 (semopy, Wishart ML) |
| 5 Validity | AVE, CR, √AVE, MSV, HTMT (bootstrap CI), Fornell–Larcker |
| 6 Method bias | Harman single factor, single-factor CFA, marker-variable adjustment (Lindell & Whitney) |
| 7 Hypotheses | Structural equation model, 5,000 percentile bootstrap CIs (seed 42), AI × DEP moderation (OLS, HC3), robustness on consented-only and outlier-free subsamples |
| 8 Extra findings | Friedman + Bonferroni-corrected Wilcoxon tests across writing phases; Gaussian mixture profiles (4 groups, diagonal covariance), entropy, Kruskal–Wallis |

## Verification result

See `VERIFICATION_REPORT.md`. In short: the data cleaning, descriptive statistics, reliability, factor analyses, model fit, validity tests, structural paths, moderation, robustness checks, phase comparison and profile means all reproduce exactly from the raw data. The report lists the few values that do not reproduce, or that are worded in a way the analysis does not support, and what to correct.
