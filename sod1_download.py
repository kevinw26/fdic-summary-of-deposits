# -*- coding: utf-8 -*-
# Copyright 2024 Kevin Wong
#
# Downloads FDIC zip files to memory; processes them into nice csv.xz files
import requests
import polars as pl

URL = 'https://www7.fdic.gov/sod/download/ALL_{}.zip'
