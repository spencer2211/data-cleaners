#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add header comments here
"""

import numpy as np
import pandas as pd
from re import search

from cleantext import CleanText as ct

# TODO: Assertion statements throughout where applicable


class CleanNumbers:

    def __init__(self, datafile):
        # TODO: Take more than just dataframes (sniffers?)
        if isinstance(datafile, pd.DataFrame):
            self.data = datafile
            self.data = ct().clean_web_text(self.data)
        else:
            print('Data not provided in DataFrame format')
            raise SystemExit(0)

    def _whole_check(self, w):
        """
        Checks if an entire series are whole number equivalents and returns the
        applicable boolean
        """
        if w.dtypes != 'object':
            self.w_check = ((w % 1) == 0).all(skipna=True)
            if self.w_check:
                return True
            else:
                return False
        else:
            return False

    def _frac_to_float(self, frac_str):
        """
        Converts and returns any applicable strings from fractions to floats

        Reference:
        https://stackoverflow.com/questions/1806278/convert-fraction-to-float/19073403#19073403
        """
        try:
            return float(frac_str)
        except ValueError:
            num, denom = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                whole = float(leading)
            except ValueError:
                whole = 0
            frac = float(num) / float(denom)
            n = whole - frac if whole < 0 else whole + frac
            return n

    def _fill_missing(self, miss, rpl_empty_with, drop_na, exceptions):
        # TODO: Add section for rpl_empty_with='NaN'
        # TODO: Separate dropna and rpl_empty_with logic
        try:
            cols = [x for x in miss.columns if x not in exceptions]
        except TypeError:
            cols = miss.columns

        if isinstance(drop_na, list):
            miss.dropna(subset=drop_na, inplace=True)
        elif drop_na:
            miss.dropna(inplace=True)
        else:
            for col in cols:
                dt = miss[col].dtypes
                m = np.nan
                if (rpl_empty_with == 'mean' and dt != 'object'):
                    m = np.mean(miss[col]).astype(dt)
                elif (rpl_empty_with == 'median' and dt != 'object'):
                    m = np.median(miss[col]).astype(dt)
                elif (rpl_empty_with == 'zeros' and dt != 'object'):
                    m = np.zeros([1])[0].astype(dt)

                miss[col] = miss[col].fillna(m)

        return miss

    def memory_reduction(self, num_mem, verbose, exceptions):
        if isinstance(num_mem, pd.DataFrame):
            start_mem = num_mem.memory_usage().sum() / 1024**2

            try:
                cols = [x for x in num_mem.columns if x not in exceptions]
            except TypeError:
                cols = num_mem.columns

            self.df = num_mem.copy()
            for col in cols:
                self.df[col] = self.df[col].replace(['', ' '], np.nan)

                # Check for fractions and convert using frac_to_float()
                self.df[col] = self.df[col].apply(
                    lambda x: self._frac_to_float(x)
                    if (isinstance(x, str)
                        and search(r'[0-9]+/[0-9]+', x))
                    else x)

                self.df[col] = pd.to_numeric(self.df[col],
                                             errors='ignore')

                if self._whole_check(self.df[col]):
                    self.df[col] = pd.to_numeric(self.df[col],
                                                 errors='ignore',
                                                 downcast='integer')
                else:
                    self.df[col] = pd.to_numeric(self.df[col],
                                                 errors='ignore',
                                                 downcast='float')

            end_mem = self.df.memory_usage().sum() / 1024**2
            reduction = (start_mem - end_mem) / start_mem
            savings = (start_mem - end_mem)

            msg = f'Mem. usage decreased to{end_mem:5.2f} MB \
({reduction * 100:.1f} % reduction) for a savings of{savings:5.2f} MB'
            if verbose:
                print(msg)

            return self.df

    def clean_numbers(self, verbose=False, rpl_empty_with='NaN',
                      drop_na=False, exceptions=None):
        # TODO: handle outliers (drop, change to avg, etc.)
        if rpl_empty_with != 'NaN':
            self.numbers = self._fill_missing(self.data,
                                              rpl_empty_with,
                                              drop_na,
                                              exceptions)
        else:
            self.numbers = self.data

        self.numbers = self.memory_reduction(self.numbers, verbose, exceptions)

        return self.numbers
