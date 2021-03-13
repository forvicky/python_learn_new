import xlrd

wb = xlrd.open_workbook("jb-2021-3-13.csv")
print("sheet 数量",wb.nsheets)
print("sheet 名称",wb.sheet_names())

sh1=wb.sheet_by_index(0)
print(u"sheet %s 共 %d 行 %d列" % (sh1.name,sh1.nrows,sh1.ncols))
print("第一行第二列的值为：",sh1.cell_value(0,1))

rows=sh1.row_values(0)
cols=sh1.col_values(1)

print("第一行的值为：",rows)
print("第二列的值为：",cols)

print("第二行第一列的值类型为：",sh1.cell(1,0).ctype)

for sh in wb.sheets():
    for r in range(sh.nrows):
        print(sh.row(r))

