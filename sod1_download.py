# -*- coding: utf-8 -*-
"""
Created on Fri 10 May 2024 00:05:26
Downloads FDIC zip files to memory; processes them into nice csv.xz files

@author: Kevin.Wong
"""
import io
import lzma
import multiprocessing as mp
import os
import re
import zipfile as zf
from concurrent.futures import ProcessPoolExecutor, wait
from datetime import datetime
from os import path

import pandas as pd
import polars as pl
import requests

URL = 'https://www7.fdic.gov/sod/download/ALL_{}.zip'
os.makedirs('sod', exist_ok=True)


def download_sod(y: int, output_path: str):
    # stream the zip archive to memory
    r = requests.get(URL.format(y))
    if r.status_code != 200:
        # warn if current year not available
        print(f'no sod file for year {y}', flush=True)
        return

    print(f'retrieved sod zip for {y}', flush=True)

    # extract the ALL file; the ALL_1 and ALL_2 files are just broken-up copies
    # of the whole data; not sure why the FDIC chose that format
    z = zf.ZipFile(io.BytesIO(r.content))
    sf_name = next(
        i for i in z.namelist() if re.match(r'ALL_\d{4}\.csv', i))

    # for unclear reasons polars doesn't like reading from the zip file handle
    # must load it all to memory first
    try:
        # in newer years utf-8 encoding is used
        sod = pd.read_csv(z.open(sf_name, 'r'), thousands=',')

    except (pl.ComputeError, UnicodeDecodeError):
        # but in earlier ears only latin-1 encoding is used
        sod = pd.read_csv(
            z.open(sf_name, 'r'), thousands=',',
            encoding='latin-1')

    # # zip can be improperly parsed as float; fix to int if so
    # if sod['ZIPBR'].dtype == float:
    #     sod = sod.with_columns(pl.col('ZIPBR').cast(pl.Int64))

    # save
    sod.to_csv(lzma.open(output_path, 'wb', preset=9))
    print(f'wrote sod {y}', flush=True)


if __name__ == '__main__':

    futures = []
    with ProcessPoolExecutor(6, mp_context=mp.get_context('spawn')) as e:
        # sod starts in 1994 --
        # there was sod prior to 1994, but it did not include thrifts; this is
        # due to FSLIC (Federal Savings and Loan Insurance Corporation) and RTC
        # (Resolution Trust Corporation) merger into the FDIC circa 1993
        for year in range(1994, datetime.now().year):
            output_path = path.join('sod', f'sod_{year}.csv.xz')
            if path.exists(output_path) and \
                    path.getsize(output_path) != 0:
                # skip files that already exist
                continue

            # download_sod(year)
            futures.append(e.submit(download_sod, year, output_path))

        wait(futures)
