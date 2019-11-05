# %%
from spacy import displacy
import zh_core_web_sm
from bs4 import BeautifulSoup
import re
import bs4
from time import sleep
import os
from datetime import datetime, timedelta
from typing import List

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
                show_debug and print('元素兄弟节点: ', [i for i in elem.fetchPreviousSiblings()], [
                                     type(i) for i in elem.fetchPreviousSiblings()])
            else:
                break

    if hasattr(elem, 'children'):
        for i in elem.children:
            unwrap(i, spec+2)


def flat_tree(elem, layer=0, nodes=None):
    if not nodes:
        nodes = []
    if len(nodes) <= layer:
        nodes.append([])
    if type(elem) == bs4.element.Tag:
        nodes[layer].append(elem)

    if not hasattr(elem, 'children'):
        return
    for i in elem.children:
        flat_tree(i, layer + 1, nodes)
    return nodes

def build_date(year=None, month=None, day=None, hour=None, minute=None):
    now = datetime.now()
    if not year:
        year = now.year
    else:
        year = int(year)
    if not month:
        month = now.month
    else:
        month = int(month)
    if not day:
        day = now.day
    else:
        day = int(day)

    if not hour:
        hour = now.hour
    else:
        hour = int(hour)
    if not minute:
        minute = now.minute
    else:
        minute = int(minute)
    return datetime(year, month, day, hour, minute)

def extract_date(text):
    for key_word, date in [
        ('本日', datetime.now().strftime("%m/%d")), 
        ('今日', datetime.now().strftime("%m/%d")),
        ('明日', (datetime.now() + timedelta(days=1)).strftime("%m/%d")),
    ]:
        text = text.replace(key_word, date)
    msg = ''
    
    res = re.findall(r'\d+', text)
    if len(res) == 2:
        mon, day = res
        msg = 'ok'
    elif len(res) > 2:
        mon, day, *left = res
        msg = 'warning'
        print(f'warning date: {text}, {res}')
    else:
        mon, day = [0, 0]
        msg = 'error'
        print(f'error date: {text}, {res}')
    return dict(date=build_date(month=mon, day=day), msg=msg)

def extract_time(text, show_debug=False):
    res = re.findall(r'\d{1,2}:\d{1,2}', text)
    msg = ''
    if len(res) == 2:
        start, end = res
        msg = 'ok'
    elif len(res) > 2:
        start, end, *left = res
        msg = 'warning'
        show_debug and print(f'warning date: {text}, {res}')
    else:
        start, end = ['00:00', '00:00']
        msg = 'error'
        show_debug and print(f'error date: {text}, {res}')
    return dict(start=start, end=end, msg=msg)


class Period:
    start: datetime = None
    end: datetime = None

    def __init__(self, date=None):
        if date:
            self.start = date
            self.end = date
    def __repr__(self):
        return self.start.strftime('%Y/%m/%d %H:%M') + '-' + self.end.strftime('%Y/%m/%d %H:%M')

    def __str__(self):
        return self.start.strftime('%Y/%m/%d %H:%M') + '-' + self.end.strftime('%Y/%m/%d %H:%M')

def clear_diff(layer):
    tags = [i.name for i in layer]
    diffs = [sum([tag_b == tag_a for tag_b in tags]) for tag_a in tags]
    for index, diff in enumerate(diffs):
        if diff == 1:
            # print(tags, diffs)
            lentags = len(tags)
            # print([diff_ for diff_ in diffs[:index] + diffs[index+1:]])
            other_diff = sum(
                [diff_ == lentags - 1 for diff_ in diffs[:index] + diffs[index+1:]]
            )
            if other_diff == lentags - 1:
                print('decompose: ', layer[index])
                layer[index].decompose()
                break

# %%
datetime.now() + timedelta(days=1)
# %%

for i in os.listdir('html'):
    filename = f'html/{i}'
    #if filename!='html/n-tengoku.com.html':
    #    continue
    with open(filename, encoding='utf-8') as f:
        html = f.read()
    for t in re.findall('(<br.*?>)', html):
        html = html.replace(t, ' ')

    bs = BeautifulSoup(html, 'html5lib')
    print(filename)
    # print_tree(bs, 0)
    unwrap(bs.body, 0, False)
    # print_tree(bs, 0)
    

    periods: List[Period] = []

    flat = flat_tree(bs)
    for layer in flat:
        if len(layer) >= 7:
            clear_diff(layer)
    flat = flat_tree(bs)

    lens = [len(i) for i in flat]

    max_index = lens.index(max(lens))
    
    max_value = lens[max_index]
    pre_value = lens[max_index - 1]

    try:
        if max_value / pre_value in [7, 8]:
            # 若干排 七八列的, 日期是表头
            k = int(max_value / pre_value)
            elems = flat[max_index]
            date = [extract_date(i.text) for i in elems[:k]]
            if all([i['msg']=='error' for i in date]):
                raise Exception('no date')
            time = [
                [extract_time(i.text) for i in elems[k:2*k]], 
                [extract_time(i.text) for i in elems[2*k:3*k]]
            ]
        elif max_value / pre_value == 2:
            # 若干排 两列的, 一列日期, 一列时间
            elems = flat[max_index]
            date = []
            time = [[]]
            index = 0
            # print(flat[max_index - 1])
            # print(elems[0], elems[1], elems[2], elems[3])
            for item in elems:
                # print(item)
                if index % 2 == 0:
                    extr = extract_date(item.text)
                    # print('data', extr)
                    if extr['msg'] == 'ok':
                        date.append(extr)
                    else:
                        continue
                else:
                    # print('time')
                    time[0].append(extract_time(item.text))
                index += 1
            print('若干排 两列的')

        else:
            # 我也不知道多少, 随缘匹配吧

            date = []
            time = [[]]
            # print_tree(bs, 0)
            # print(elems)
            # print('我也不知道多少, 随缘匹配吧')
            


        if date[0]['msg'] == 'ok' and all([i['msg']=='error' for i in date[1:]]):
            for i in range(len(date[1:])):
                date[i+1]['date'] = date[0]['date'] + timedelta(days=1)

        flag = False
        for time_ in time:
            for index, item in enumerate(time_):
                if item['msg'] == 'ok':
                    period = Period(date[index]['date'])

                    hour, minute = [int(i) for i in item['start'].split(':')]
                    period.start -= timedelta(hours=period.start.hour)
                    period.start += timedelta(hours=hour)
                    period.start -= timedelta(minutes=period.start.minute)
                    period.start += timedelta(minutes=minute)
                    hour, minute = [int(i) for i in item['end'].split(':')]
                    period.end -= timedelta(hours=period.end.hour)
                    period.end += timedelta(hours=hour)
                    period.end -= timedelta(minutes=period.end.minute)
                    period.end += timedelta(minutes=minute)

                    periods.append(period)
                    flag = True
            if flag:
                break
        print(periods)

    except Exception as e:
        print(e)
    # break


# %%
