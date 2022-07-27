import tushare as ts
import pandas as pd

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', None)

ts.set_token('bea67662261d745b6c338c30abd05e8b8d7d59798b566fd6fa5024ff')

pro = ts.pro_api()

df = pro.daily(ts_code='600141.SH', start_date='20220701', end_date='20220714')

print(df)