#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add header comments here
"""

import numpy as np
import pandas as pd
from re import search


class CleanNumbers:

    def __init__(self, datafile):
        # TODO: assertion statements
        self.verbose = False

        # TODO: add file/data type sniffer logic
        if isinstance(datafile, pd.DataFrame):
            self.data = datafile
        else:
            print('Data not provided in DataFrame format')
            # TODO: Learn how to place a brake here
            raise SystemExit(0)

    def _whole_check(self, w):
        # TODO: assertion statements
        """
        Checks if an entire series are whole number equivalents and returns the
        applicable boolean
        """
        if not isinstance(w.any(), str):
            self.w_check = ((w % 1) == 0).all()
            if self.w_check:
                return True
            else:
                return False
        else:
            return False

    def _frac_to_float(self, frac_str):
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

    def _fill_missing(self, miss, replace_with):
        # TODO: Fix mean/median datatypes
        for col in miss.columns:
            m = np.nan
            if (replace_with == 'mean'
                    and miss[col].dtypes != 'object'):
                m = miss[col].mean().astype(miss[col].dtypes)
                # m = m.astype(miss[col].dtypes)
            elif (replace_with == 'median'
                    and miss[col].dtypes != 'object'):
                m = miss[col].median().round().astype(miss[col].dtypes)
                # m = m.astype(miss[col].dtypes)
            elif (replace_with == 'zero'
                    and miss[col].dtypes != 'object'):
                m = np.zeros([1])[0].astype(miss[col].dtypes)
                # m = m.astype(miss[col].dtypes)

            miss[col] = miss[col].fillna(m)
            print(m)

        return miss

    def memory_redux(self, num_mem, verbose=False):
        # TODO: assertion statements
        if verbose:
            self.verbose = verbose

        if isinstance(num_mem, pd.DataFrame):
            start_mem = num_mem.memory_usage().sum() / 1024**2

            self.df = num_mem.copy()
            for col in self.df.columns:
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
            if self.verbose:
                print(msg)

            return self.df

    def clean_numbers(self, verbose=False, replace_with='NaN'):
        # TODO: assertion statements
        # Handle missing numbers (fill with avg, drop rows, etc.)
        # handle outliers (drop, change to avg, etc.)
        if verbose:
            self.verbose = verbose

        # TODO: place edge case pre-check here
        self.numbers = self.memory_redux(self.data, self.verbose)
        if replace_with != 'NaN':
            self.numbers = self._fill_missing(self.numbers, replace_with)

        return self.numbers
