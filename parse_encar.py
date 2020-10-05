import pandas as pd
import csv
from pprint import pprint

FNAME = '_encar_new.csv'
names = [
    'ts',
    'transmission',
    'fuel',
    'color',
    'category',
    'price',
    'make',
    'year',
    'month',
    'state',
    'car_id',
    'model_name',
    'model_trim',
    'model',
    'desc1',
    'desc2',
]

df = pd.read_csv(FNAME, header=None, names=names, index_col=False)

def strip_col(val) -> str:
    if type(val) == str:
        return val.strip().replace('  ', ' ')
    return val

def get_views(val) -> int:
    val = val.split('조회수')[1]
    val = val.split('자세히보기')[0]
    val = val.replace(',', '')
    return int(val.strip())

def get_likes(val) -> int:
    val = val.split('찜')[1]
    val = val.replace(',', '')
    return int(val.strip())

for name in names:
    df[name] = df.apply(lambda x: strip_col(x.get(name)), axis=1)

df['views'] = df.apply(lambda x: get_views(x.get('desc2')), axis=1)
df['likes'] = df.apply(lambda x: get_likes(x.get('desc2')), axis=1)
del df['desc1']
del df['desc2']

car_ids = df.car_id.unique()

raw_values = [
    'transmission',
    'fuel',
    'color',
    'category',
    'price',
    'make',
    'year',
    'month',
    'state',
    'car_id',
    'model_name',
    'model_trim',
    'model',
]
min_maxs = [['car_id', 'views', 'likes', 'ts_min', 'ts_max'] + raw_values]
for id in car_ids:
    df_id = df[df['car_id'] == id]
    first_vals = [df_id[n].iloc[0] for n in raw_values]
    min_maxs.append([
        id,
        df_id['views'].max(),
        df_id['likes'].max(),
        df_id['ts'].min(),
        df_id['ts'].max(),
    ] + first_vals)

names[-2] = 'views'
names[-1] = 'likes'
df.to_csv('encar_views_likes.csv', index=False, header=names)
with open('encar_ts_min_max.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(min_maxs)
