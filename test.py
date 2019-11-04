# %%
from spacy import displacy
import zh_core_web_sm
from bs4 import BeautifulSoup
import re

# %%
nlp = zh_core_web_sm.load()
# %%
def print_nlp(doc):
    for token in doc:
        print(token.text, token.ent_type_)

# %%
doc = nlp("2019年二月三十号")
print_nlp(doc)

# %%
import os
with open('html/chin2-t.com.html', encoding='utf-8') as f:
    html = f.read()

# %%
bs = BeautifulSoup(html,'html5lib')
bs
# %%
def iuli(text):
    for i in '\n\r ':
        text = text.replace(i, '')
    return text

# %%
def dpdd(elem):
    if hasattr(elem, 'children'):
        for i in elem.children:
            dpdd(i)
    else:
        text = iuli(elem)
        if text:
            print_nlp(nlp(text))
            print('*'*10)

dpdd(bs)
print('end')
# %%
m = re.match(r"(?P<mon>\d+(?=月))", "10月2日")
m.groupdict()

# %%
m = re.search(r"(?P<mon>\d+(?=月))(?P<day>\d+(?=日))+", "10月2日")
m.groupdict()