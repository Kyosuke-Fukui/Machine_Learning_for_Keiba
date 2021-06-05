import urllib.request
import urllib.parse
import re
import json
import pandas as pd
import seaborn as sns
import numpy as np

url = 'https://oldrace.netkeiba.com/?pid=show_ninkioddsgraph_js&raceid=201905050811&type={0}&offset=0&limit=5000'
ngscore = 0

# 各買い方のスコアを出し買い方によって偏りがないか
# スコアはオッズに確率（馬の実力完全無視）をかけたもの


def santan(url):

    url = url.format('8')

    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        score_arr = np.array([0] * len(umalist))
        count_arr = np.array([0] * len(umalist))

        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            score = float(odd['odds'])*(1/(len(umalist) *
                                           (len(umalist)-1)*(len(umalist)-2)))
            score_arr[int(kumi[0]) - 1] += score
            score_arr[int(kumi[1]) - 1] += score
            score_arr[int(kumi[2]) - 1] += score
            count_arr[int(kumi[0]) - 1] += 1
            count_arr[int(kumi[1]) - 1] += 1
            count_arr[int(kumi[2]) - 1] += 1

        score_arr = score_arr/count_arr

        score_arr = [ngscore if i == 0 else i for i in score_arr]
        df = pd.DataFrame(data={'3tan': score_arr}, columns=['3tan'])
        return df

    except Exception as e:
        print(e)
        return []


def sanfuku(url):

    url = url.format('7')
    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        score_arr = np.array([0] * len(umalist))
        count_arr = np.array([0] * len(umalist))

        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            score = float(odd['odds'])*(6/(len(umalist) *
                                           (len(umalist)-1)*(len(umalist)-2)))
            score_arr[int(kumi[0]) - 1] += score
            score_arr[int(kumi[1]) - 1] += score
            score_arr[int(kumi[2]) - 1] += score
            count_arr[int(kumi[0]) - 1] += 1
            count_arr[int(kumi[1]) - 1] += 1
            count_arr[int(kumi[2]) - 1] += 1

        score_arr = score_arr/count_arr

        score_arr = [ngscore if i == 0 else i for i in score_arr]
        df = pd.DataFrame(data={'3fuku': score_arr}, columns=['3fuku'])
        return df

    except Exception as e:
        print(e)
        return []


def umatan(url):

    url = url.format('6')

    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        score_arr = np.array([0] * len(umalist))
        count_arr = np.array([0] * len(umalist))

        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            score = float(odd['odds'])*(1/(len(umalist) * (len(umalist)-1)))
            score_arr[int(kumi[0]) - 1] += score
            score_arr[int(kumi[1]) - 1] += score
            count_arr[int(kumi[0]) - 1] += 1
            count_arr[int(kumi[1]) - 1] += 1

        score_arr = score_arr/count_arr

        score_arr = [ngscore if i == 0 else i for i in score_arr]
        df = pd.DataFrame(data={'umatan': score_arr}, columns=['umatan'])
        return df

    except Exception as e:
        print(e)
        return []


def umaren(url):

    url = url.format('4')

    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        score_arr = np.array([0] * len(umalist))
        count_arr = np.array([0] * len(umalist))

        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            score = float(odd['odds'])*(2/(len(umalist) * (len(umalist)-1)))
            score_arr[int(kumi[0]) - 1] += score
            score_arr[int(kumi[1]) - 1] += score
            count_arr[int(kumi[0]) - 1] += 1
            count_arr[int(kumi[1]) - 1] += 1

        score_arr = score_arr/count_arr

        score_arr = [ngscore if i == 0 else i for i in score_arr]

        df = pd.DataFrame(data={'umaren': score_arr}, columns=['umaren'])
        return df

    except Exception as e:
        print(e)
        return []


def wide(url):

    url = url.format('5')

    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        score_arr = np.array([0] * len(umalist))
        count_arr = np.array([0] * len(umalist))

        for odd in res['showArray']:
            kumi = odd['Kumi'].split('-')
            # オッズがレンジなので上限と下限の平均を得点とする
            odds_range = list(
                map(float, (re.findall(r"[-+]?\d*\.\d+|\d+", odd['odds']))))
            score = sum(odds_range)/len(odds_range) * \
                (6/(len(umalist) * (len(umalist)-1)))
            score_arr[int(kumi[0]) - 1] += score
            score_arr[int(kumi[1]) - 1] += score
            count_arr[int(kumi[0]) - 1] += 1
            count_arr[int(kumi[1]) - 1] += 1

        score_arr = score_arr/count_arr

        score_arr = [ngscore if i == 0 else i for i in score_arr]
        df = pd.DataFrame(data={'wide': score_arr}, columns=['wide'])
        return df

    except Exception as e:
        print(e)
        return []


def tanfuku(url):

    url = url.format('1')
    try:

        with urllib.request.urlopen(url) as f:
            res = json.loads(f.read().decode('utf-8'))

        o1 = []
        tan = []
        fuku = []
        for odd in res['showArray']:
            o1.append(odd['Kumi'])
            tan.append(float(odd['tan']))
            odds_range = list(map(float, re.findall(
                r"[-+]?\d*\.\d+|\d+", odd['fuku'])))
            fuku.append(sum(odds_range)/len(odds_range))

        tan = list(map(lambda x: x*(1/len(o1)), tan))
        fuku = list(map(lambda x: x*(3/len(o1)), fuku))
        umalist, tan, fuku = zip(*sorted(zip(o1, tan, fuku)))

        return umalist, tan, fuku

    except Exception as e:
        print(e)
        return [], [], []


(umalist, tan, fuku) = tanfuku(url)
df = pd.DataFrame(data={
    'umaban': umalist,
    'tan': tan,
    'fuku': fuku
}, columns=[
    'umaban',
    'tan',
    'fuku'
])
df2 = df.join(umaren(url)).join(wide(url)).join(
    umatan(url)).join(sanfuku(url)).join(santan(url))

cm = sns.light_palette("#2ecc71", as_cmap=True)
df2.style.background_gradient(cmap=cm)

print(df2)
# print(df2.to_html())
