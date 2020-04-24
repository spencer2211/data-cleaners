#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add header comments here
"""

import pandas as pd
import re as re
from bs4 import BeautifulSoup as bs

# TODO: Assertion statements where applicable

# Test sample data
# HTML = ['<div>\n\thello\n</div>', {'<div>\nhola\n </div>': ['2nd', '\n\n']}]
HTML = pd.DataFrame([{'Greeting': '<div>\n\tHELLO\n</div>',
                      'Position': ['1st\n', '2nd', 1]},
                     {'Greeting': '<div>\nHOLA\n </div>',
                      'Position': '1/2\n\n'}])


class CleanText:
    """
    Class to execute common text cleaning task in general/serialized fashion.

    Current implementation:
    - web test cleaning
    - common erroneous charter cleaning

    Future implementation:
    - xml text clean (replace/remove namespaces)
    """

    def __init__(self):
        pass

    def _clean_nl(self, nl_text):
        """
        Removes newline, carriage return, tabs, and erroneous spaces and
        returns the result
        """
        self.rpl_txt = re.sub(r'\\s+', ' ', nl_text)
        to_replace = [r'\n', r'\t', r'\r']

        for trpl in to_replace:
            self.rpl_txt = re.sub(trpl, '', self.rpl_txt)

        self.rpl_txt = self.rpl_txt.strip()

        return self.rpl_txt

    def clean_web_text(self, web_text=HTML):
        """
        Removes common web text tags and returns the result
        """

        if isinstance(web_text, pd.DataFrame):
            self.df = web_text.copy()
            self.df = self.df.applymap(
                lambda text: bs(text, 'html.parser').get_text()
                if isinstance(text, str) else text
            )

            self.df = self.df.applymap(
                lambda text2: self.clean_web_text(text2)
            )

            return self.df

        elif isinstance(web_text, list):
            self.list_txt = []
            for e in web_text:
                self.cl = CleanText()
                self.list_txt.append(self.cl.clean_web_text(e))

            return self.list_txt

        elif isinstance(web_text, dict):
            self.dict_txt = {}
            for k, v in web_text.items():
                self.dict_txt[self.clean_web_text(k)] = self.clean_web_text(v)

            return self.dict_txt

        elif isinstance(web_text, (set, frozenset)):
            self.set_txt = set()
            for s in web_text:
                self.set_txt.add(self.clean_web_text(s))

            return self.set_txt

        elif isinstance(web_text, tuple):
            self.tuple_txt = [
                bs(text, 'html.parser').get_text()
                if isinstance(text, str)
                else self.clean_web_text(text) for text in web_text]
            self.tuple_txt = tuple(self.tuple_txt)

            return self.tuple_txt

        elif isinstance(web_text, str):
            self.new_txt = bs(web_text, 'html.parser').get_text()
            self.new_txt = self._clean_nl(self.new_txt)

            return self.new_txt

        elif isinstance(web_text, (int, float, complex)):
            self.n = web_text

            return self.n
