# TODO: Create standard header ###
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs

html = [r'<div>\nhello\n</div>', {r'<div>\nhola\n</div>': [r'2nd', r'\n\n']}]


class CleanText:

    def __init__(self):
        pass
    
    def clean_nl(self, nl_text):
        self.nl_txt = nl_text.replace(r'\n', '')

        return self.nl_txt

    def clean_web_text(self, wb_txt=html):
        self.web_text = wb_txt
        checked = self.tc.check(self.web_text)

        if isinstance(self.web_text, pd.DataFrame):
            self.df = self.web_text.copy()
            self.df = df.applymap(
                lambda text: bs(text, 'html.parser').get_text()
                if isinstance(text, str) else text)

            # self.df = df.replace(r'\\n', '', regex=True)
            # self.df = df.replace('', np.nan)

            return self.df

        elif isinstance(self.web_text, list):
            self.list_txt = []       
            for e in self.web_text:
                self.cl = CleanText()
                self.list_txt.append(self.cl.clean_web_text(e))

            return self.list_txt

        elif isinstance(self.web_text, dict):
            self.dict_txt = {}
            for k,v in self.web_text.items():
                self.dict_txt[self.clean_web_text(k)] = self.clean_web_text(v)
            
            return self.dict_txt
        
        elif isinstance(self.web_text, (set, frozenset)):
            self.set_txt = set()
            for s in self.web_text:
                self.set_txt.add(self.clean_web_text(s))
            
            return self.set_txt

        elif isinstance(self.web_text, tuple):
            self.tuple_txt = [
                bs(text, 'html.parser').get_text()
                if isinstance(text, str)
                else self.clean_web_text(text) for text in self.web_text]
            self.tuple_txt = tuple(self.tuple_txt)

            return self.tuple_txt

        elif isinstance(self.web_text, str):
            self.new_txt = bs(self.web_text, 'html.parser').get_text()
            self.new_txt = self.clean_nl(self.new_txt)

            return self.new_txt
        
        elif isinstance(self.web_text, (int, float, complex)):
            self.n = self.web_text

            return self.n
