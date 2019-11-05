# %%
from spacy import displacy
import zh_core_web_sm
from bs4 import BeautifulSoup
import re
import bs4
from time import sleep
import os
# %%

def print_tree(elem, spec=0):
    if elem.name:
        print('-'*spec, elem.name)
    if hasattr(elem, 'children'):
        for i in elem.children:
            print_tree(i, spec+2)
with open(r'html\yuzuki-club.com.html', encoding='utf-8') as f:
    html = f.read()
bs = BeautifulSoup(html, 'html5lib')
print_tree(bs)
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
def unwrap(elem, spec=0, show_debug=False):
    if elem.name:
        
        show_debug and print('当前元素: ', elem)
        show_debug and print('元素兄弟节点: ', get_bro_by_parents(elem, True))
        while all(
            [type(i) != bs4.element.Tag for i in get_bro_by_parents(elem)]
        ):
            children = list(elem.children)
            if all([type(i) != bs4.element.Tag for i in children]):
                parents = list(elem.parents)[0]
                show_debug and print('解包前', bs)
                elem.unwrap()
                show_debug and print('解包后', bs)
                elem = parents
                show_debug and print('当前元素: ', elem)
                show_debug and print('元素兄弟节点: ', [i for i in elem.fetchPreviousSiblings()], [type(i) for i in elem.fetchPreviousSiblings()])
            else:
                break

    if hasattr(elem, 'children'):
        for i in elem.children:
            unwrap(i, spec+2)


# %%
for i in os.listdir('html'):
    filename = f'html/{i}'
    with open(filename, encoding='utf-8') as f:
        html = f.read()
    for t in re.findall('(<br.*?>)', html):
        html = html.replace(t, ' ')

    bs = BeautifulSoup(html, 'html5lib')
    print(filename)
    print_tree(bs, 0)
    unwrap(bs.body, 0, False)
    print_tree(bs, 0)
    break

