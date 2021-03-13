import csv
import pandas as pd
import numpy as np

# with open('jb-2021-3-13.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     col7 = [row[7] for row in reader]
#     col9 = [row[9] for row in reader]
#     print(col7)
#     print(col9)

data1 = pd.read_csv('jb-2021-3-13.csv', usecols=['电话1'],encoding='gbk')
data2 = pd.read_csv('jb-2021-3-13.csv', usecols=['电话2'],encoding='gbk')

data1 = np.array(data1)
data2 = np.array(data2)

print(data1)
print(data2)