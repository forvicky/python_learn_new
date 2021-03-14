import pandas as pd
import os

def clean_data(dataframe):
    result = dataframe.sort_values('电话1')  # inplace=True则result原来的顺序被改变，否则改变的是返回值
    print("排序后================\n",result)
    result = result.drop_duplicates()
    result = result.dropna()
    print("去重去nan后================\n",result)
    print('电话号码数据类型=',result['电话1'].dtype)
    isTel = result['电话1'].astype(str).str.contains('^1[3-9]\d{9}$')
    print(isTel)
    filter = result[isTel]
    print("过滤后================\n",filter)
    return filter

def jb_csv(filename):
    df1 = pd.read_csv(filename, usecols=['电话1'], encoding='gbk',na_filter=False)
    df2 = pd.read_csv(filename, usecols=['电话2'], encoding='gbk',na_filter=False)

    print(df1)
    print(df2)
    df2.columns = ['电话1']
    print(df2)

    result = pd.concat([df1, df2])  # 拼接列名相同的列
    print("拼接后================\n",result)
    result['电话1'].astype('str')
    return result

def ds_csv(filename):
    df1 = pd.read_csv(filename, usecols=['电话1'], encoding='gbk',na_filter=False) #关闭NAN，只有空值，NAN会导致类型转化失败
    df2 = pd.read_csv(filename, usecols=['电话2'], encoding='gbk',na_filter=False)
    df3 = pd.read_csv(filename, usecols=['电话3'], encoding='gbk',na_filter=False)

    print(df1)
    print(df2)
    print(df3)
    df2.columns = ['电话1']
    df3.columns = ['电话1']
    print(df2)
    print(df3)

    result = pd.concat([df1, df2, df3])  # 拼接列名相同的列
    print("拼接后================\n",result)
    result['电话1'].astype('str')
    return result


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f

def main():
    base = './'
    jb_list=[]
    ds_list=[]
    for i in findAllFile(base):
        print(i)
        if i.startswith('ds') and i.endswith('.csv'):
            ds_list.append(i)
        elif i.startswith('jb') and i.endswith('.csv'):
            jb_list.append(i)
    #"""
    jb_df_list=[]
    for jb in jb_list:
        print(jb)
        jb_df = jb_csv(jb)
        jb_df_list.append(jb_df)

    result = pd.concat(jb_df_list)  # 拼接列名相同的列
    jb_df_clean = clean_data(result)
    jb_df_clean.to_csv('../result/jb_result.csv', index=False, header=False)  # index是否保存索引，header是否保存列名

    ds_df_list=[]
    for ds in ds_list:
        ds_df = ds_csv(ds)
        ds_df_list.append(ds_df)

    result = pd.concat(ds_df_list)  # 拼接列名相同的列
    ds_df_clean = clean_data(result)
    ds_df_clean.to_csv('../result/ds_result.csv', index=False, header=False)
    #"""
    df_list=[]
    for jb in jb_list:
        print(jb)
        jb_df = jb_csv(jb)
        df_list.append(jb_df)

    for ds in ds_list:
        ds_df = ds_csv(ds)
        df_list.append(ds_df)

    result = pd.concat(df_list)  # 拼接列名相同的列
    df_clean = clean_data(result)
    df_clean.to_csv('../result/all_result.csv', index=False, header=False)

if __name__ == '__main__':
    main()