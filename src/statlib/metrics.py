import numpy as np
import math
import scipy.stats
from scipy.stats import chi2


def expectation(z):
    return sum(z) / len(z)


def dispersion(z):
    mx = expectation(z)
    return sum((z - mx) ** 2) / (len(z) - 1)


def conditional_expectation(x, y):
    n = len(x)
    return sum(x[i] * y[i] for i in range(n)) / n


def get_bins_count(n):
    if n <= 100:
        return int(np.sqrt(n))
    return 4 * int(np.log(n))


def get_val_counts(arr):
    counts = {}
    for x in arr:
        counts[x] = counts.get(x, 0) + 1

    return counts


def build_distribution_function(x_var):
    counts = get_val_counts(x_var)

    F = [0]
    for i in range(len(x_var) - 1):
        F.append(F[i] + counts[x_var[i]] / n)

    return F


def generate_borders(x_var, segments):
    n = len(x_var)
    res = [x_var[0]]
    for i in range(n // segments - 1, n - 1, n // segments):
        res.append((x_var[i] + x_var[i + 1]) / 2)
    res.append(x_var[-1])
    return res


def pearson_chi(bins, vals, F, n):
    chi = 0
    for i in range(len(bins) - 1):
        if not vals[i]:
            continue

        l = bins[i]
        r = bins[i + 1]
        pi_s = F(r) - F(l)
        pi = vals[i]
        chi += (pi - pi_s)**2 / pi_s

    return chi * n


def get_dispersion_borders(s, alpha, n):
    l = s * (n - 1) / chi2.ppf(1 - alpha / 2, n - 1)
    r = s * (n - 1) / chi2.ppf(alpha / 2, n - 1)
    return l, r


def get_dispersion_borders_known(s, alpha, n):
    l = s * n / chi2.ppf(1 - alpha / 2, n)
    r = s * n / chi2.ppf(alpha / 2, n)
    return l, r


def get_dispersion_interval(x_var, alpha):
    m_p = expectation(x_var)
    d_p = dispersion(x_var)

    return get_dispersion_borders(d_p, alpha, len(x_var))


def get_exp_interval(s, val, n):
    return s * scipy.stats.norm.ppf(val) / np.sqrt(n)
