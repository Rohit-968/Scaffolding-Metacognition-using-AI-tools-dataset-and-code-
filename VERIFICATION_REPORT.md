# Verification Report — Data Analysis Summary

Every statistic in *From Scaffolding to Dependency · Data Analysis Summary* (October 2026) was re-computed from the untouched raw export (`data/raw/responses_csv.csv`) with `analysis.py`. The re-computed values are in `results/computed_values.csv`.

**Status key:** ✅ reproduces exactly (to the reported decimals) · ⚠️ reproduces, but wording or rounding needs a small fix · ❌ does not reproduce

## Overall assessment

**Share with corrections.** Apart from the twelve items in the table below, every reported value reproduces exactly, including every estimate the hypothesis decisions rest on. Six bootstrap confidence intervals and one normality statistic in the summary do not reproduce and should be replaced, and three statements need rewording. None of these changes any hypothesis decision: H1, H3 and H5 remain supported, and H2 and H4 remain unsupported.

## Corrections required

| # | Where | Reported | Re-computed | Severity | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | §7 hypothesis table, H1 CI | .74 to .87 | .66 to .85 | ❌ High | Replace |
| 2 | §7 hypothesis table, H2 CI | −.11 to .25 | −.18 to .24 | ❌ High | Replace (still includes 0) |
| 3 | §7 hypothesis table and mediation table, H3 indirect via scaffolding CI | .38 to .68 | .31 to .67 | ❌ High | Replace (still excludes 0) |
| 4 | §7 hypothesis table and mediation table, H5 direct CI | .01 to .30 | .04 to .41 | ❌ High | Replace (still excludes 0) |
| 5 | §7 mediation table, indirect via metacognition CI | −.09 to .20 | −.14 to .19 | ❌ High | Replace (still includes 0) |
| 6 | §7 mediation table, total effect CI | .64 to .82 | .60 to .80 | ❌ High | Replace |
| 7 | §1 Mardia normalised value | 3.78 | 63.91 (34 items); 60.24 (31 items) | ❌ Medium | Replace with 63.91. The conclusion (data not multivariate normal, so bootstrapping is used) is unchanged and becomes stronger |
| 8 | §8 "BIC chose 4 groups" | BIC chose 4 | BIC keeps falling after 4 (4: 4369.37, 5: 4367.23, 6: 4329.58, 7: 4320.40); lowest at 7 | ⚠️ Medium | Say the 4-profile solution was chosen for interpretability; BIC did not single it out. The revised manuscript already words this correctly |
| 9 | §8 "93% of students share high dependency worry" | 93% | 93.4% of students are in the three user groups, whose *average* DEP is 5.03–5.34. Individually, 58.0% of all students (62.2% of AI users) average ≥ 5 on DEP | ⚠️ Medium | Rephrase, e.g. "All three AI-user groups (93% of students) average above 5 on dependency costs" |
| 10 | §7 extra path AI → DEP | p = .005 | p = .0055 | ⚠️ Low | Report p = .006 (or p < .01) |
| 11 | Figure 5 title vs §5 text | .15–.28 vs .14–.28 | META–DEP r = .145 | ⚠️ Low | Use one value in both places (.14–.28) |
| 12 | §4 CFA table, M3 description | "5 factors but scaffolding + writing merged" | Merging SCF and AW leaves 4 factors (AI, META, SCF+AW, DEP) on 31 items | ⚠️ Low | Rename to "4 factors, scaffolding + writing merged, 31 items" |

The six intervals in rows 1–6 were re-estimated with 5,000 percentile bootstrap resamples (seed 42). The re-computed intervals agree with Tables 7 and 8 of the revised manuscript (e.g. H1 [.665, .844], indirect via scaffolding [.299, .662]) to within normal bootstrap variation, so the manuscript tables are correct and the Summary values appear to come from an earlier run.

## Section-by-section check

### 1. Data cleaning and normality

| Value | Reported | Re-computed | Status |
| --- | --- | --- | --- |
| Raw responses / date range | 303, 15 Jun – 9 Oct 2026 | 303, 15 Jun – 9 Oct 2026 | ✅ |
| Duplicates removed | 6 → 297 | 6 → 297 | ✅ |
| Incomplete removed (> 3 blank) | 5 → 292 | 5 → 292 | ✅ |
| Straight-liners removed | 6 → 286 | 6 → 286 | ✅ |
| Blank answers imputed (median) | 15 (0.15%) | 15 (0.15%) | ✅ |
| Outliers kept | 25 | 25 (Mahalanobis D², p < .001) | ✅ |
| Item skewness | −1.22 to −0.24 | −1.22 to −0.24 | ✅ |
| Item kurtosis | −0.92 to 1.16 | −0.92 to 1.16 | ✅ |
| Mardia normalised | 3.78 | 63.91 | ❌ (row 7) |

Note for the reviewer: all six "duplicates" are copies of straight-lined responses (rows 70, 88, 134 copy row 66, all 4s; rows 106, 288 copy row 92, all 7s; row 210 copies row 17, all 1s). The count of removed responses is correct either way, but these may be repeated careless responses rather than one person submitting twice. Full detail is in `changes_log.csv`.

### 2. Descriptive statistics

| Construct | Mean | SD | 95% CI | % agree | d | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AI tool usage | 5.25 | 1.34 | 5.10–5.41 | 68.9 | 0.94 | ✅ |
| Metacognitive awareness | 4.73 | 1.36 | 4.57–4.89 | 49.7 | 0.54 | ✅ |
| Perceived AI scaffolding | 4.88 | 1.39 | 4.72–5.04 | 58.0 | 0.63 | ✅ |
| Writing skills & confidence | 4.79 | 1.49 | 4.61–4.96 | 55.9 | 0.53 | ✅ |
| Perceived dependency costs | 5.09 | 1.45 | 4.92–5.26 | 59.8 | 0.75 | ✅ |
| Worry about over-reliance | 5.29 | 1.63 | 5.10–5.48 | 68.2 | 0.79 | ✅ |

All six t-tests against 4 give p < .001 ✅. All 34 item-level "% agree" values in Figure 1 reproduce exactly, including AI3 = 83% (highest) and META1 = 50% (lowest) ✅.

### 3. Reliability

| Construct | α main | ω | Item–total r | Status |
| --- | --- | --- | --- | --- |
| AI tool usage | .921 | .922 | .67–.81 | ✅ |
| Metacognitive awareness | .897 | .899 | .57–.76 | ✅ |
| Perceived AI scaffolding | .930 | .931 | .72–.81 | ✅ |
| Writing skills & confidence | .919 | .921 | .77–.86 | ✅ |
| Perceived dependency costs | .874 | .875 | .57–.81 | ✅ |

DEP α without AW5 = .899 ✅. Pilot α values (N = 54) cannot be checked because the pilot data are not in this repository.

### 4. Factor structure

| Value | Reported | Re-computed | Status |
| --- | --- | --- | --- |
| KMO | .934 | .934 | ✅ |
| Bartlett χ²(561) | 7636.8, p < .001 | 7636.8, p < .001 | ✅ |
| Eigenvalues 1–4 | 14.75, 3.47, 1.82, 1.74 | 14.75, 3.47, 1.82, 1.74 | ✅ |
| Factors retained (parallel analysis) | 4 | 4 | ✅ |
| AW5–AW8 form their own EFA factor | Yes | Yes (loadings .53–.89) | ✅ |

| Model | χ²/df | CFI | TLI | RMSEA | SRMR | Status |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 6.26 | .627 | .603 | .136 | .106 | ✅ |
| M1 | 4.47 | .757 | .738 | .110 | .092 | ✅ |
| M2 | 3.05 | .857 | .845 | .085 | .077 | ✅ |
| M3 | 3.12 | .868 | .856 | .086 | .062 | ✅ (label: row 12) |
| M4 | 2.60 | .901 | .892 | .075 | .058 | ✅ |

M4 vs M3 Δχ²(4) = 234.0, p < .001 ✅. Dropped-item loadings META8 .47, META9 .53, META10 .48 ✅. All 31 loadings in Figure 4 reproduce, 29 ≥ .70 ✅.

### 5. Convergent and discriminant validity

| Construct | AVE | CR | √AVE | Status |
| --- | --- | --- | --- | --- |
| AI tool usage | .597 | .922 | .773 | ✅ |
| Metacognitive awareness | .563 | .899 | .750 | ✅ |
| Perceived AI scaffolding | .626 | .931 | .791 | ✅ |
| Writing skills & confidence | .744 | .921 | .862 | ✅ |
| Perceived dependency costs | .647 | .875 | .804 | ✅ |

Latent correlations in Figure 5 (AI–META .77, AI–SCF .74, AI–AW .71, META–SCF .79, META–AW .70, SCF–AW .82, DEP .14–.28) ✅. HTMT all < .85, highest SCF–AW .826, bootstrap CI .738–.899 (reported .736–.899, within bootstrap variation) ✅. Fornell–Larcker fails for exactly AI–META, META–SCF and SCF–AW ✅.

### 6. Common method bias

| Value | Reported | Re-computed | Status |
| --- | --- | --- | --- |
| Harman first factor | 43–46% | 43.4% (34 items), 46.2% (31 items) | ✅ |
| Single-factor CFA | CFI .667, Δχ²(10) = 1616.0 | CFI .667, Δχ²(10) = 1616.0 | ✅ |
| Marker (smallest r) | .17 | .174 | ✅ |
| Marker-adjusted benefit r | .56–.71 | .559–.714 | ✅ |

### 7. Structural model and hypotheses

| Value | Reported | Re-computed | Status |
| --- | --- | --- | --- |
| Fit | χ²(427) = 1114.4, CFI .900, RMSEA .075, SRMR .064 | χ²(427) = 1114.4, CFI .8996, RMSEA .075, SRMR .064 | ✅ |
| R² writing / metacognition / scaffolding | 70% / 59% / 54% | 69.5% / 58.8% / 54.2% | ✅ |
| H1 AI → META | β .77, p < .001 | β .767, p < .001 | ✅ |
| H2 META → AW | β .02, p = .789 | β .023, p = .789 | ✅ |
| AI → SCF / SCF → AW | .74 / .64 | .736 / .635 | ✅ |
| H3 indirect via SCF | β .47 | β .468 | ✅ |
| H4 AI × DEP | β .003, p = .926 | standardised β .0031, b .0024, p = .926 | ✅ |
| H4 CI | −.05 to .06 | −.055 to .059 | ✅ |
| H5 AI → AW | β .22, p = .002 | β .224, p = .002 | ✅ |
| AI → DEP | β .18, p = .005 | β .180, p = .0055 | ⚠️ (row 10) |
| Mediation shares | 66% / 2% / 32% | 66% / 2% / 32% | ✅ |
| Simple slopes (low / mean / high DEP) | 0.69 / 0.69 / 0.70 | 0.691 / 0.694 / 0.698 | ✅ |
| Bootstrap CIs for H1, H2, H3, H5, META indirect, total | see rows 1–6 | see rows 1–6 | ❌ |

CFI of the structural model is .8996, so it rounds to .900 but sits on the cut-off; "acceptable" is the right word, as the summary already says.

**Robustness table** — every entry reproduces ✅:

| Path | All (286) | Consent (192) | No outliers (261) |
| --- | --- | --- | --- |
| AI → META | .77*** | .74*** | .80*** |
| META → AW | .02 | −.04 | .05 |
| AI → SCF | .74*** | .75*** | .76*** |
| SCF → AW | .64*** | .78*** | .58*** |
| AI → AW | .22** | .09 | .24** |
| AI → DEP | .18** | .06 | .20** |
| AI × DEP | .002 | .037 | −.007 |

### 8. Extra findings

| Value | Reported | Re-computed | Status |
| --- | --- | --- | --- |
| Friedman χ²(2) | 52.1, p < .001 | 52.1, p < .001 | ✅ |
| Planning / monitoring / reflection | 4.50 / 5.03 / 4.52 | 4.50 / 5.03 / 4.52 | ✅ |
| Wilcoxon effect sizes | r = .42, .33 | r = .42, .33 | ✅ |
| META8 mean | 5.49 | 5.49 | ✅ |
| Profile sizes | 92 / 92 / 83 / 19 | 92 / 92 / 83 / 19 | ✅ |
| Profile means (all 20 values) | Table in §8 | Identical | ✅ |
| Entropy | .84 | .840 | ✅ |
| BIC chose 4 | Yes | No (row 8) | ⚠️ |
| Kruskal–Wallis DEP | H(3) = 14.1, p = .003 | H(3) = 14.1, p = .003 | ✅ |
| Driven only by non-adopters | Yes | Among the three user groups H(2) = 3.4, p = .187 | ✅ |
| 93% share high dependency worry | 93% | See row 9 | ⚠️ |

## Consistency with the revised manuscript

The revised manuscript (`From_Scaffolding_to_Dependency_Revised.docx`) was also compared with the re-computed values. Its Tables 4–11 reproduce (one small exception: Table 7 gives z = 2.80 for AI → DEP; re-computed z = 2.78), but it disagrees with the Summary, and once with itself, in these places:

| Topic | Summary | Manuscript | Re-computed | Action |
| --- | --- | --- | --- | --- |
| Bootstrap CIs | Rows 1–6 above | Table 7 and Table 8 values | Agree with manuscript tables | Update the Summary |
| §4.4 manuscript text | — | Text gives [.38, .68], [−.09, .20], [.01, .30]; Table 8 on the same page gives [.299, .662], [−.144, .180], [.043, .406] | Agrees with Table 8 | Correct the §4.4 paragraph to match Table 8 |
| H4 p-value | .926 (ordinary SE) | .936 (HC3 robust SE) | Both correct for their method | Use the same method in both documents |
| Table 9 simple-slope SEs | — | Text says HC3; the SEs and t-values shown (0.06 / 0.05 / 0.07) are ordinary OLS | HC3 SEs would be 0.064 / 0.069 / 0.095 | Either state OLS or replace with HC3 values |
| Marker test | Reported (r = .17 marker) | "Marker-based adjustment was not possible" | Post-hoc marker reproduces | Decide whether to report it, and align both documents |
| BIC for profiles | "BIC chose 4" | "Alternative solutions had lower BIC" | Manuscript is correct | Update the Summary |
| Smallest profile name | Non-adopters | Infrequent users | — | Use one name |
| Sample description | "One engineering college" | Students aged 18–25 recruited mainly in India; link may have reached other universities | Not checkable from the data | Use one description |

## Values that cannot be checked from this data

The pilot reliabilities (N = 54), and any claim about age, institution or country, are not recorded in `responses_csv.csv`.

## Notes on the code in the Summary appendix

The appendix code reproduces the cleaning, descriptives, reliability, EFA, final CFA, AVE/CR, HTMT, SEM, moderation, phase tests and profiles. `analysis.py` adds the steps the appendix leaves out: Mardia's test, parallel analysis, models M0–M3 and the single-factor CFA, the outlier rule, Harman and marker tests, bootstrap intervals for every path, robustness re-runs, HC3 errors, BIC comparison and entropy. Two practical issues with the appendix code: `factor_analyzer` 0.5.1 fails with scikit-learn 1.6 or later unless patched (handled at the top of `analysis.py`), and the appendix bootstrap returns only the two indirect effects, so the other intervals in the hypothesis table cannot be produced from it as written.
