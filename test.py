# %%
from spacy import displacy
import zh_core_web_sm
from bs4 import BeautifulSoup
import re
import bs4
from time import sleep
import os
# %%
# nlp = zh_core_web_sm.load()
# # %%
# def print_nlp(doc):
#     for token in doc:
#         print(token.text, token.ent_type_)

# # %%
# doc = nlp("2019年二月三十号")
# print_nlp(doc)

# # %%
# import os
# with open('html/chin2-t.com.html', encoding='utf-8') as f:
#     html = f.read()

# # %%
# bs = BeautifulSoup(html,'html5lib')
# bs
# # %%
# def iuli(text):
#     for i in '\n\r ':
#         text = text.replace(i, '')
#     return text

# # %%
# def dpdd(elem):
#     if hasattr(elem, 'children'):
#         for i in elem.children:
#             dpdd(i)
#     else:
#         text = iuli(elem)
#         if text:
#             print_nlp(nlp(text))
#             print('*'*10)

# dpdd(bs)
# print('end')
# # %%
# m = re.match(r"(?P<mon>\d+(?=月))", "10月2日")
# m.groupdict()

# # %%
# m = re.search(r"(?P<mon>\d+(?=月))*.*(?P<day>\d+(?=日))*", "10月2日")
# m.groupdict()

# # %%
# text = "10月23日"

# m = re.findall(r"(?P<mon>\d+\W*(?=月))", text)
# print(m)

# m = re.findall(r"(?P<day>\d+\W*(?=日))", text)
# print(m)


# %%

def test(elem, spec):
    # print(type(elem), end='-')
    if elem.name:
        print('-'*spec, elem.name)
    # print()

    if hasattr(elem, 'children'):
        for i in elem.children:
            test(i, spec+2)
with open(r'html\yuzuki-club.com.html', encoding='utf-8') as f:
    html = f.read()
bs = BeautifulSoup(html)
test(bs, 0)
# %%
t = '''
<tr>
    <td width="45" bgcolor="#9b9fcf" scope="col">
        <div align="center">
            <font color="#FFFFFF" size="2">11/04<br>(月) </font>
        </div>
    </td>
    <td width="45" bgcolor="#9b9fcf" scope="col">
        <div align="center">
            <font color="#FFFFFF" size="2">11/05<br>(火) </font>
        </div>
    </td>
</tr>
'''
bs = BeautifulSoup(t, 'html5lib')
# %%
def izip(*iters):
    for iter_ in iters:
        if iter_:
            for i in iter_:
                yield i
def get_bro_by_parents(elem, Tag=False):
    parents = next(elem.parents)
    ret = []
    for i in parents.children:
        if i is elem:
            continue
        if Tag and type(i) != bs4.element.Tag:
            continue
        ret.append(i)
    return ret
# %%
def test3(elem, spec):
    if elem.name:
        
        # print('当前元素: ', elem)
        # print('元素兄弟节点: ', get_bro_by_parents(elem, True))
        while all(
            [type(i) != bs4.element.Tag for i in get_bro_by_parents(elem)]
        ):
            children = list(elem.children)
            if all([type(i) != bs4.element.Tag for i in children]):
                parents = list(elem.parents)[0]
                # print('解包前', bs)
                elem.unwrap()
                # print('解包后', bs)
                elem = parents
                # print('当前元素: ', elem)
                # print('元素兄弟节点: ', [i for i in elem.fetchPreviousSiblings()], [type(i) for i in elem.fetchPreviousSiblings()])
            else:
                break

    if hasattr(elem, 'children'):
        for i in elem.children:
            test3(i, spec+2)


# %%
for i in os.listdir('html'):
    filename = f'html/{i}'

    with open(filename, encoding='utf-8') as f:
        html = f.read()
    bs = BeautifulSoup(html, 'html5lib')
    print(filename)
    test(bs, 0)
    test3(bs.body, 0)
    test(bs, 0)

'''
html/cityheaven.net.html
html/yesgrp.com.html
'''