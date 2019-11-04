# %%
from spacy import displacy
import zh_core_web_sm
from bs4 import BeautifulSoup
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
        print([ord(i) for i in text])
        if text:
            print(text)
            print('*'*10)

dpdd(bs)
print('end')
# %%
