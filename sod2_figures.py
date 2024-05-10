# -*- coding: utf-8 -*-
"""
Created on Fri 10 May 2024 00:40:54
Reads downloaded SOD data and plots two charts:
    - Branch and deposit HHI box plots
    - Box plot of main office deposits over time

@author: Kevin.Wong
"""
import lzma
import os
from glob import glob
from os import path

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns
from matplotlib import ticker

os.makedirs('figs', exist_ok=True)
sod = pl.concat(
    (pl.read_csv(lzma.open(i), infer_schema_length=None) for i in
     glob(path.join('sod', 'sod*.csv.xz'))),
    how='diagonal_relaxed'
).sort(by=['YEAR', 'CERT', 'BRNUM'])
print('read sod')

# -----------------------------------------------------------------------------
# calculate hhi

cert = sod.group_by(['YEAR', 'STCNTYBR', 'CERT']).agg(
    pl.col('BRNUM').count().alias('BRS'),
    pl.col('DEPSUMBR').sum().alias('DEP'))
cnty = sod.group_by(['YEAR', 'STCNTYBR']).agg(
    pl.col('BRNUM').count().alias('BRS'),
    pl.col('DEPSUMBR').sum().alias('DEP')
)
cert = (
    cert.join(cnty, on=['YEAR', 'STCNTYBR'], suffix='_cnty')
    .sort(by=['YEAR', 'STCNTYBR', 'CERT'])
    .with_columns(
        (pl.col('BRS') / pl.col('BRS_cnty')).alias('BRS_mksh'),
        (pl.col('DEP') / pl.col('DEP_cnty')).alias('DEP_mksh')
    )
)

hhi = cert.group_by(['YEAR', 'STCNTYBR']).agg(
    (pl.col('BRS_mksh') * 100).pow(2).sum().alias('BRS_hhi'),
    (pl.col('DEP_mksh') * 100).pow(2).sum().alias('DEP_hhi')
).sort(by=['YEAR', 'STCNTYBR']).to_pandas()
print('calc hhi')

# -----------------------------------------------------------------------------
# calculate main office share

mo_dep = (
    sod.group_by(['YEAR', 'CERT', 'BKMO'])
    .agg(pl.col('DEPSUMBR').sum())
    .pivot(index=['YEAR', 'CERT'], columns='BKMO', values='DEPSUMBR')
    .fill_null(0)
    .sort(by=['YEAR', 'CERT'])
    .to_pandas()
)
mo_dep.set_index(['YEAR', 'CERT'], inplace=True)
mo_dep['total'] = mo_dep.sum(axis=1)
mo_dep['mo_share'] = 100 * (mo_dep['1'] / mo_dep['total'])
print('calc mo share')

# -----------------------------------------------------------------------------
# plot main office share
lims = (hhi['YEAR'].min() - 0.75, hhi['YEAR'].max() + 0.75)
hhi_f, (hhi_l, hhi_r) = plt.subplots(1, 2, figsize=(8, 4))
sns.boxplot(x='YEAR', y='BRS_hhi', ax=hhi_l, data=hhi, native_scale=True)
sns.boxplot(x='YEAR', y='DEP_hhi', ax=hhi_r, data=hhi, native_scale=True,
            color='tab:orange')
hhi_l.set(xlabel='', ylabel='Branch HHI', xlim=lims, ylim=(0, 10_000))
hhi_r.set(xlabel='', ylabel='Deposit HHI', xlim=lims, ylim=(0, 10_000))
hhi_r.yaxis.tick_right()
hhi_r.yaxis.set_label_position('right')
for ax in [hhi_l, hhi_r]:
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2_000))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1_000))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.grid(ls='dotted', axis='y')
hhi_f.tight_layout()
hhi_f.suptitle('Branch and deposit HHI distribution over time')
hhi_f.subplots_adjust(top=0.92)
hhi_f.savefig(path.join('figs', 'sod branch and deposit hhis.png'))
print('saved hhi figure')

mos_f, mos_a = plt.subplots(figsize=(8, 8))
sns.boxplot(
    x='YEAR', y='mo_share', data=mo_dep, ax=mos_a, native_scale=True,
    color='tab:green',  # inner='quart'
)
mos_a.set(
    xlabel='', ylabel='% of deposits at main office', xlim=lims, ylim=(0, 100),
    title='% of "branch deposits" at main office over time')
mos_a.yaxis.set_major_locator(ticker.MultipleLocator(10))
mos_a.yaxis.set_minor_locator(ticker.MultipleLocator(5))
mos_a.xaxis.set_major_locator(ticker.MultipleLocator(5))
mos_a.xaxis.set_minor_locator(ticker.MultipleLocator(1))
mos_a.grid(ls='dotted', axis='y')
mos_f.tight_layout()
mos_f.savefig(path.join('figs', 'sod deposit pc at main office.png'))
print('saved mo share figure')
