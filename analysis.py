import warnings, numpy as np, pandas as pd, semopy, statsmodels.api as sm
from scipy import stats
from sklearn.utils import check_array
import factor_analyzer.factor_analyzer as fa_mod
fa_mod.check_array = lambda X, **k: check_array(X, **{("ensure_all_finite" if a == "force_all_finite" else a): b for a, b in k.items()})
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")

N_BOOT = 5000
OUT = []
def rec(section, name, value):
    OUT.append((section, name, value)); print(f"[{section}] {name}: {value}")

raw = pd.read_csv("data/raw/responses_csv.csv")
codes = [f"AI{i}" for i in range(1, 9)] + [f"META{i}" for i in range(1, 11)] + [f"SCF{i}" for i in range(1, 9)] + [f"AW{i}" for i in range(1, 9)]
pd.DataFrame({"code": codes, "item_text": [c.strip() for c in raw.columns[2:]]}).to_csv("data/processed/codebook.csv", index=False)

d = raw.iloc[:, 2:].apply(lambda s: s.str[0].astype(float)); d.columns = codes
d.insert(0, "row", np.arange(1, len(d) + 1)); d.insert(1, "timestamp", raw.Timestamp); d.insert(2, "consent", raw.iloc[:, 1].notna())
log = []
dup = d[codes].duplicated()
for i in d.index[dup]:
    first = d.index[(d[codes].fillna(-1) == d.loc[i, codes].fillna(-1)).all(axis=1)][0]
    log.append((d.row[i], d.timestamp[i], "removed", "duplicate", f"identical on all 34 items to row {d.row[first]}"))
d = d[~dup]
inc = d[codes].isna().sum(axis=1) > 3
for i in d.index[inc]: log.append((d.row[i], d.timestamp[i], "removed", "incomplete", f"{int(d.loc[i, codes].isna().sum())} of 34 items blank"))
d = d[~inc]
flat = d[codes].nunique(axis=1) == 1
for i in d.index[flat]: log.append((d.row[i], d.timestamp[i], "removed", "straight-lining", f"answered {int(d.loc[i, codes].dropna().iloc[0])} on every item"))
d = d[~flat]
med = d[codes].median()
for i, c in zip(*np.where(d[codes].isna())):
    log.append((d.row.iloc[i], d.timestamp.iloc[i], "imputed", codes[c], f"blank -> item median {med[codes[c]]:g}"))
d[codes] = d[codes].fillna(med)
d = d.reset_index(drop=True)
rec("1 Cleaning", "raw responses", len(raw)); rec("1 Cleaning", "duplicates removed", int(dup.sum()))
rec("1 Cleaning", "incomplete removed", int(inc.sum())); rec("1 Cleaning", "straight-liners removed", int(flat.sum()))
rec("1 Cleaning", "final N", len(d)); rec("1 Cleaning", "cells imputed", sum(1 for l in log if l[2] == "imputed"))
rec("1 Cleaning", "imputed share of answers (%)", round(100 * sum(1 for l in log if l[2] == "imputed") / (len(d) * 34), 2))
rec("1 Cleaning", "consent recorded (final sample)", int(d.consent.sum()))

X = d[codes].values; Xc = X - X.mean(0)
md = np.einsum("ij,jk,ik->i", Xc, np.linalg.inv(np.cov(X.T)), Xc)
d["mv_outlier"] = md > stats.chi2.isf(.001, 34)
for i in d.index[d.mv_outlier]: log.append((d.row[i], d.timestamp[i], "flagged (kept)", "multivariate outlier", f"Mahalanobis D2 = {md[i]:.1f} (p < .001, df = 34)"))
rec("1 Cleaning", "multivariate outliers flagged (kept)", int(d.mv_outlier.sum()))
pd.DataFrame(log, columns=["raw_row", "timestamp", "action", "reason", "detail"]).sort_values(["action", "raw_row"], key=lambda c: c.map({"removed": 0, "imputed": 1, "flagged (kept)": 2}) if c.name == "action" else c).to_csv("data/processed/changes_log.csv", index=False)

rec("1 Normality", "item skewness range", f"{d[codes].skew().min():.2f} to {d[codes].skew().max():.2f}")
rec("1 Normality", "item kurtosis range", f"{d[codes].kurt().min():.2f} to {d[codes].kurt().max():.2f}")
n, p = X.shape; S = np.cov(X.T, bias=True); D = Xc @ np.linalg.inv(S) @ Xc.T
b2 = np.mean(np.diag(D) ** 2)
rec("1 Normality", "Mardia kurtosis b2 (34 items)", round(b2, 2))
rec("1 Normality", "Mardia normalised z (34 items)", round((b2 - p * (p + 2)) / np.sqrt(8 * p * (p + 2) / n), 2))

C = {"AI": [f"AI{i}" for i in range(1, 9)], "META": [f"META{i}" for i in range(1, 8)], "SCF": [f"SCF{i}" for i in range(1, 9)],
     "AW": ["AW1", "AW2", "AW3", "AW4"], "DEP": ["AW5", "AW6", "AW7", "AW8"]}
K = list(C); it31 = sum(C.values(), [])
comp = pd.DataFrame({k: d[v].mean(axis=1) for k, v in C.items()}); comp["WORRY"] = d[["META9", "META10"]].mean(axis=1)
def alpha(x): k = x.shape[1]; return k / (k - 1) * (1 - x.var().sum() / x.sum(axis=1).var())

ag = (d[codes] >= 5).mean() * 100
for c in codes: rec("2 Item % agree", c, round(ag[c]))
for k in comp:
    c = comp[k]; t = stats.ttest_1samp(c, 4); ci = t.confidence_interval()
    rec("2 Constructs", f"{k} mean / SD", f"{c.mean():.2f} / {c.std():.2f}")
    rec("2 Constructs", f"{k} 95% CI", f"{ci.low:.2f}-{ci.high:.2f}")
    rec("2 Constructs", f"{k} % agree (mean >= 5)", round(100 * (c >= 5).mean(), 1))
    rec("2 Constructs", f"{k} t(285), p", f"{t.statistic:.2f}, {t.pvalue:.1e}")
    rec("2 Constructs", f"{k} Cohen d vs 4", round((c.mean() - 4) / c.std(), 2))
    rec("2 Constructs", f"{k} skew / kurtosis", f"{c.skew():.2f} / {c.kurt():.2f}")

for k, v in C.items():
    itc = [d[v].sum(axis=1).sub(d[i]).corr(d[i]) for i in v]
    rec("3 Reliability", f"{k} alpha", round(alpha(d[v]), 3)); rec("3 Reliability", f"{k} item-total r", f"{min(itc):.2f}-{max(itc):.2f}")
rec("3 Reliability", "DEP alpha without AW5", round(alpha(d[["AW6", "AW7", "AW8"]]), 3))

rec("4 EFA", "KMO", round(calculate_kmo(d[codes])[1], 3))
chi, pb = calculate_bartlett_sphericity(d[codes]); rec("4 EFA", "Bartlett chi2(561), p", f"{chi:.1f}, {pb:.1e}")
ev = np.linalg.eigvalsh(d[codes].corr().values)[::-1]
rng = np.random.default_rng(0)
p95 = np.percentile([np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((n, p)).T))[::-1] for _ in range(1000)], 95, axis=0)
rec("4 EFA", "first 5 eigenvalues", ", ".join(f"{e:.2f}" for e in ev[:5]))
rec("4 EFA", "parallel analysis 95th pct (first 5)", ", ".join(f"{e:.2f}" for e in p95[:5]))
rec("4 EFA", "factors retained", int(np.argmax(ev < p95)))
pd.DataFrame(FactorAnalyzer(4, rotation="oblimin").fit(d[codes]).loadings_, index=codes, columns=["F1", "F2", "F3", "F4"]).round(3).to_csv("results/efa_loadings.csv")

spec = lambda M: "\n".join(f"{k} =~ " + " + ".join(v) for k, v in M.items())
def srmr(m, data, items):
    S = data[items].cov().values; Sig = m.calc_sigma()[0]; ob = m.vars["observed"]
    ix = [ob.index(i) for i in items]; Sig = Sig[np.ix_(ix, ix)]
    a, b = np.sqrt(np.diag(S)), np.sqrt(np.diag(Sig))
    return np.sqrt(np.mean((S / np.outer(a, a) - Sig / np.outer(b, b))[np.tril_indices(len(items))] ** 2))
def fitstats(M, data):
    m = semopy.Model(M if isinstance(M, str) else spec(M)); m.fit(data, obj="MLW"); s = semopy.calc_stats(m).T["Value"]
    items = it31 if isinstance(M, str) else sum(M.values(), [])
    return m, dict(chi2=s.chi2, df=s.DoF, CFI=s.CFI, TLI=s.TLI, RMSEA=s.RMSEA, SRMR=srmr(m, data, items))
MODELS = {
    "M0 one factor, 34 items": {"G": codes},
    "M1 original 4 sections, 34 items": {"AI": C["AI"], "META": [f"META{i}" for i in range(1, 11)], "SCF": C["SCF"], "AW": [f"AW{i}" for i in range(1, 9)]},
    "M2 5 factors, worry items as DEP, 34 items": {"AI": C["AI"], "META": [f"META{i}" for i in range(1, 9)], "SCF": C["SCF"], "AW": C["AW"], "DEP": ["META9", "META10"] + C["DEP"]},
    "M3 SCF+AW merged (4 factors), 31 items": {"AI": C["AI"], "META": C["META"], "SCFAW": C["SCF"] + C["AW"], "DEP": C["DEP"]},
    "M4 final 5 factors, 31 items": C,
    "Single factor, 31 items": {"G": it31}}
fits = {}
for name, M in MODELS.items():
    m, f = fitstats(M, d); fits[name] = f
    rec("4 CFA", name, f"chi2({f['df']:.0f}) = {f['chi2']:.1f}, chi2/df = {f['chi2'] / f['df']:.2f}, CFI = {f['CFI']:.3f}, TLI = {f['TLI']:.3f}, RMSEA = {f['RMSEA']:.3f}, SRMR = {f['SRMR']:.3f}")
    if name.startswith("M2"):
        e = m.inspect(std_est=True)
        for i in ["META8", "META9", "META10"]: rec("4 CFA", f"M2 loading {i}", round(float(e[(e.op == "~") & (e.lval == i)]["Est. Std"].iloc[0]), 2))
    if name.startswith("M4"): cfa = m
a, b = fits["M3 SCF+AW merged (4 factors), 31 items"], fits["M4 final 5 factors, 31 items"]
rec("4 CFA", "M4 vs M3 delta chi2", f"{a['chi2'] - b['chi2']:.1f} (df {a['df'] - b['df']:.0f}), p = {stats.chi2.sf(a['chi2'] - b['chi2'], a['df'] - b['df']):.1e}")

e = cfa.inspect(std_est=True); L = e[(e.op == "~") & e.rval.isin(C)]
L[["lval", "rval", "Est. Std", "p-value"]].rename(columns={"lval": "item", "rval": "construct", "Est. Std": "std_loading"}).to_csv("results/cfa_loadings.csv", index=False)
rec("5 Validity", "items with loading >= .70", int((L["Est. Std"] >= .70).sum()))
lat = e[(e.op == "~~") & e.lval.isin(C) & e.rval.isin(C) & (e.lval != e.rval)]
lr = {frozenset((x, y)): float(r) for x, y, r in zip(lat.lval, lat.rval, lat["Est. Std"])}
sq = {}
for k in C:
    l = L[L.rval == k]["Est. Std"].values.astype(float); ave = np.mean(l ** 2); sq[k] = np.sqrt(ave)
    rec("5 Validity", f"{k} AVE / CR(=omega) / sqrtAVE / MSV", f"{ave:.3f} / {l.sum() ** 2 / (l.sum() ** 2 + np.sum(1 - l ** 2)):.3f} / {sq[k]:.3f} / {max(r ** 2 for s, r in lr.items() if k in s):.3f}")
R = d[it31].corr()
def htmt(R, x, y):
    m = lambda c: R.loc[C[c], C[c]].values[np.triu_indices(len(C[c]), 1)].mean()
    return R.loc[C[x], C[y]].values.mean() / np.sqrt(m(x) * m(y))
for i, x in enumerate(K):
    for y in K[i + 1:]:
        r = lr[frozenset((x, y))]
        rec("5 Validity", f"{x}-{y} latent r / HTMT / Fornell-Larcker", f"{r:.3f} / {htmt(R, x, y):.3f} / {'fail' if r > min(sq[x], sq[y]) else 'pass'}")
rng = np.random.default_rng(42); Xi = d[it31].values
hb = [htmt(pd.DataFrame(Xi[rng.integers(0, n, n)], columns=it31).corr(), "SCF", "AW") for _ in range(N_BOOT)]
rec("5 Validity", "HTMT SCF-AW bootstrap 95% CI", f"{np.percentile(hb, 2.5):.3f}-{np.percentile(hb, 97.5):.3f}")

rec("6 Method bias", "Harman: first component share, 34 items (%)", round(100 * ev[0] / 34, 1))
rec("6 Method bias", "Harman: first component share, 31 items (%)", round(100 * np.linalg.eigvalsh(d[it31].corr().values)[-1] / 31, 1))
a = fits["Single factor, 31 items"]
rec("6 Method bias", "single-factor vs M4 delta chi2", f"{a['chi2'] - b['chi2']:.1f} (df {a['df'] - b['df']:.0f})")
cr = comp[K].corr(); rM = cr.values[np.triu_indices(5, 1)].min(); adj = (cr - rM) / (1 - rM)
ben = [adj.loc[x, y] for i, x in enumerate(K[:4]) for y in K[i + 1:4]]
rec("6 Method bias", "marker r (smallest composite r)", round(rM, 3))
rec("6 Method bias", "marker-adjusted benefit r range", f"{min(ben):.3f}-{max(ben):.3f}")

SEM = spec(C) + "\nMETA ~ AI\nSCF ~ AI\nAW ~ AI + META + SCF\nDEP ~ AI\nMETA ~~ SCF"
PATHS = [("META", "AI"), ("SCF", "AI"), ("AW", "META"), ("AW", "SCF"), ("AW", "AI"), ("DEP", "AI")]
def sem_paths(data):
    m = semopy.Model(SEM); m.fit(data, obj="MLW"); e = m.inspect(std_est=True)
    g = lambda l, r: float(e[(e.op == "~") & (e.lval == l) & (e.rval == r)]["Est. Std"].iloc[0])
    v = {f"{r}->{l}": g(l, r) for l, r in PATHS}
    v["indirect via SCF"] = v["AI->SCF"] * v["SCF->AW"]; v["indirect via META"] = v["AI->META"] * v["META->AW"]
    v["total indirect"] = v["indirect via SCF"] + v["indirect via META"]; v["total"] = v["total indirect"] + v["AI->AW"]
    return m, e, v
m, e, est = sem_paths(d); s = semopy.calc_stats(m).T["Value"]
rec("7 SEM", "fit", f"chi2({s.DoF:.0f}) = {s.chi2:.1f}, chi2/df = {s.chi2 / s.DoF:.2f}, CFI = {s.CFI:.3f}, TLI = {s.TLI:.3f}, RMSEA = {s.RMSEA:.3f}, SRMR = {srmr(m, d, it31):.3f}")
for k in ["META", "SCF", "AW", "DEP"]:
    rec("7 SEM", f"R2 {k}", round(1 - float(e[(e.op == "~~") & (e.lval == k) & (e.rval == k)]["Est. Std"].iloc[0]), 3))
st = e[(e.op == "~") & e.lval.isin(C) & e.rval.isin(C)]
for _, r in st.iterrows(): rec("7 SEM", f"{r.rval}->{r.lval} beta / SE / z / p", f"{r['Est. Std']:.3f} / {r['Std. Err']:.3f} / {r['z-value']:.2f} / {r['p-value']:.4f}")
for k in ["indirect via SCF", "indirect via META", "total indirect", "total"]: rec("7 SEM", k, round(est[k], 3))
for k in ["indirect via SCF", "indirect via META", "AI->AW"]: rec("7 SEM", f"share of total: {k} (%)", round(100 * est[k] / est["total"]))
rng = np.random.default_rng(42); B = []
for i in range(N_BOOT):
    B.append(sem_paths(d.sample(n, replace=True, random_state=rng.integers(1e9)).reset_index(drop=True))[2])
    if i % 500 == 0: print("bootstrap", i, flush=True)
B = pd.DataFrame(B); B.to_csv("results/sem_bootstrap_draws.csv", index=False)
for k in B: rec("7 SEM bootstrap", f"{k} 95% CI", f"{B[k].quantile(.025):.3f} to {B[k].quantile(.975):.3f}")

def moderation(c):
    X = pd.DataFrame({"AI": c.AI - c.AI.mean(), "DEP": c.DEP - c.DEP.mean()}); X["INT"] = X.AI * X.DEP
    return X, sm.OLS(c.AW, sm.add_constant(X)).fit()
X, o = moderation(comp); h = o.get_robustcov_results("HC3")
z = (comp - comp.mean()) / comp.std()
bz = sm.OLS(z.AW, sm.add_constant(pd.DataFrame({"AI": z.AI, "DEP": z.DEP, "INT": z.AI * z.DEP}))).fit().params
rec("7 Moderation", "AI x DEP b / SE / p (OLS)", f"{o.params.INT:.4f} / {o.bse.INT:.3f} / {o.pvalues.INT:.3f}")
rec("7 Moderation", "AI x DEP SE / p (HC3)", f"{h.bse[3]:.3f} / {h.pvalues[3]:.3f}")
rec("7 Moderation", "AI x DEP standardised beta", round(bz.INT, 4)); rec("7 Moderation", "DEP standardised beta", round(bz.DEP, 3))
rng = np.random.default_rng(42); Xv, yv = sm.add_constant(X).values, comp.AW.values
bi = [np.linalg.lstsq(Xv[j], yv[j], rcond=None)[0][3] for j in (rng.integers(0, n, n) for _ in range(N_BOOT))]
rec("7 Moderation", "AI x DEP bootstrap 95% CI", f"{np.percentile(bi, 2.5):.3f} to {np.percentile(bi, 97.5):.3f}")
V = np.asarray(o.cov_params())
for lab, zz in [("-1 SD", -1), ("mean", 0), ("+1 SD", 1)]:
    g = np.array([0, 1, 0, zz * X.DEP.std()]); sl, se = g @ o.params.values, np.sqrt(g @ V @ g)
    rec("7 Moderation", f"simple slope at {lab} DEP (b / SE / t)", f"{sl:.3f} / {se:.3f} / {sl / se:.2f}")
X2 = pd.DataFrame({"SCF": comp.SCF - comp.SCF.mean(), "DEP": comp.DEP - comp.DEP.mean()}); X2["INT"] = X2.SCF * X2.DEP
o2 = sm.OLS(comp.AW, sm.add_constant(X2)).fit(); rec("7 Moderation", "SCF x DEP b / p (exploratory)", f"{o2.params.INT:.3f} / {o2.pvalues.INT:.3f}")

for lab, sub in [("consent recorded", d[d.consent]), ("outliers removed", d[~d.mv_outlier])]:
    sub = sub.reset_index(drop=True); m, e, v = sem_paths(sub); sec = f"7 Robustness ({lab}, N = {len(sub)})"
    for l, r in PATHS: rec(sec, f"{r}->{l}", f"{v[f'{r}->{l}']:.3f} (p = {float(e[(e.op == '~') & (e.lval == l) & (e.rval == r)]['p-value'].iloc[0]):.3f})")
    _, o3 = moderation(pd.DataFrame({k: sub[v2].mean(axis=1) for k, v2 in C.items()})); rec(sec, "AI x DEP b (p)", f"{o3.params.INT:.4f} ({o3.pvalues.INT:.3f})")
    _, f = fitstats(C, sub); rec(sec, "CFA M4 CFI / RMSEA / SRMR", f"{f['CFI']:.3f} / {f['RMSEA']:.3f} / {f['SRMR']:.3f}")

P, Mo, Rf = d[["META1", "META2", "META3"]].mean(axis=1), d[["META4", "META5", "META6"]].mean(axis=1), d["META7"]
rec("8 Phases", "planning / monitoring / reflection means", f"{P.mean():.2f} / {Mo.mean():.2f} / {Rf.mean():.2f}")
f = stats.friedmanchisquare(P, Mo, Rf); rec("8 Phases", "Friedman chi2(2), p", f"{f.statistic:.1f}, {f.pvalue:.1e}")
for lab, x, y in [("planning vs monitoring", P, Mo), ("monitoring vs reflection", Mo, Rf), ("planning vs reflection", P, Rf)]:
    w = stats.wilcoxon(x, y); rec("8 Phases", f"Wilcoxon {lab}: Bonferroni p / r", f"{min(1, 3 * w.pvalue):.1e} / {stats.norm.isf(w.pvalue / 2) / np.sqrt(n):.2f}")
rec("8 Phases", "META8 mean", round(d.META8.mean(), 2))

bic = {k: GaussianMixture(k, covariance_type="diag", n_init=20, random_state=0).fit(comp[K]).bic(comp[K]) for k in range(1, 9)}
rec("8 Profiles", "BIC by k (raw composites)", ", ".join(f"{k}: {v:.2f}" for k, v in bic.items()))
rec("8 Profiles", "k with lowest BIC (k = 1-8)", min(bic, key=bic.get))
zs = StandardScaler().fit_transform(comp[K])
bs = {k: GaussianMixture(k, covariance_type="diag", n_init=20, random_state=0).fit(zs).bic(zs) for k in range(1, 9)}
rec("8 Profiles", "BIC by k (standardised composites)", ", ".join(f"{k}: {v:.2f}" for k, v in bs.items()))
gm = GaussianMixture(4, covariance_type="diag", n_init=20, random_state=0).fit(comp[K])
comp["profile"] = gm.predict(comp[K]); pr = gm.predict_proba(comp[K])
rec("8 Profiles", "entropy", round(1 + np.sum(pr * np.log(np.clip(pr, 1e-300, 1))) / (n * np.log(4)), 3))
order = comp.groupby("profile").AI.mean().sort_values(ascending=False).index
names = dict(zip(order, ["Engaged & aware", "Pragmatic users", "Ambivalent users", "Non-adopters"]))
comp["profile"] = comp.profile.map(names)
for g, r in comp.groupby("profile")[K].mean().loc[list(names.values())].iterrows():
    k = (comp.profile == g).sum(); rec("8 Profiles", g, f"n = {k} ({100 * k / n:.0f}%), " + ", ".join(f"{c} = {r[c]:.2f}" for c in K))
kw = stats.kruskal(*[comp.DEP[comp.profile == g] for g in names.values()]); rec("8 Profiles", "Kruskal-Wallis DEP, 4 groups", f"H(3) = {kw.statistic:.1f}, p = {kw.pvalue:.3f}")
kw = stats.kruskal(*[comp.DEP[comp.profile == g] for g in list(names.values())[:3]]); rec("8 Profiles", "Kruskal-Wallis DEP, 3 user groups", f"H(2) = {kw.statistic:.1f}, p = {kw.pvalue:.3f}")
rec("8 Profiles", "share in the three user groups (%)", round(100 * (comp.profile != "Non-adopters").mean(), 1))

out = d[["row", "timestamp", "consent", "mv_outlier"] + codes].rename(columns={"row": "raw_row"})
out[[c if c != "WORRY" else "WORRY_META9_10" for c in comp.columns]] = comp.round(4).values
out.to_csv("data/processed/cleaned_data.csv", index=False)
pd.DataFrame(OUT, columns=["section", "statistic", "computed_value"]).to_csv("results/computed_values.csv", index=False)
