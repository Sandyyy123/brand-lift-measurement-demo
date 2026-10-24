"""Synthetic paired randomized geography incrementality illustration; stdlib only."""
from itertools import product
from math import isfinite
from statistics import mean


def analyze(rows):
    """Equal-pair mean change contrast; exact two-sided sharp-null sign-flip test.

    Assumes one treated and one control geography per randomized pair, equal
    independent assignment probability, no spillover, and fixed observed outcomes
    under the sharp null. Counts are illustrative equal-duration outcomes, not
    population-normalized rates. No causal inference from arbitrary observational
    before/after data is implied.
    """
    if not 2 <= len(rows) <= 18:
        raise ValueError('Require 2–18 randomized pairs for exact enumeration')
    if len({r['pair'] for r in rows}) != len(rows):
        raise ValueError('Duplicate pair identifiers')
    keys = ('treated_pre','treated_post','control_pre','control_post')
    for r in rows:
        if any(not isinstance(r[k],(int,float)) or not isfinite(r[k]) or r[k]<0 for k in keys):
            raise ValueError('Outcomes must be finite nonnegative numbers')
    contrasts = [(r['treated_post']-r['treated_pre'])-(r['control_post']-r['control_pre']) for r in rows]
    effect = mean(contrasts)
    count = sum(abs(sum(s*x for s,x in zip(signs,contrasts))/len(rows)) >= abs(effect)-1e-10 for signs in product((-1,1),repeat=len(rows)))
    naive = mean(r['treated_post']-r['treated_pre'] for r in rows)
    control_change = mean(r['control_post']-r['control_pre'] for r in rows)
    return {'pairs':len(rows),'mean_change_contrast':effect,'naive_treated_change':naive,
            'mean_control_change':control_change,'exact_two_sided_p':count/2**len(rows),
            'assignments_enumerated':2**len(rows),'pair_contrasts':contrasts,
            'estimand':'Equal-pair mean incremental outcome count per geography over the period',
            'null':'Sharp null of no effect in any geography; independent within-pair randomization'}


def synthetic_fixture():
    # Fixed deterministic illustrative contrasts. No client information.
    contrasts = [-3,4,6,7,8,9,9,10,11,12,13,22]
    return [{'pair':i+1,'treated_pre':100+10*i,'treated_post':100+10*i+20+c,
             'control_pre':105+10*i,'control_post':105+10*i+20}
            for i,c in enumerate(contrasts)]
