import pandas as pd

path = '大连.json'
df = pd.read_json(path)

res_df = pd.DataFrame()
res_df['公司名称'] = df['name']
res_df['公司类型'] = df['type']
res_df['公司人数'] = df['employers_count']
res_df['所在行业'] = df['industry']
res_df['公司地址'] = df['address']
res_df['公司官网'] = df['website']
res_df['公司简介'] = df['introduction']

res_df.to_excel('大连.xlsx')
