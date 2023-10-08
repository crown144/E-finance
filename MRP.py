import pyodbc
import pandas as pd
import datetime as dt
import tkinter as tk
import math

#数据库连接
coon = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-4EJQ0G73;DATABASE=MRP;UID=sa;PWD=1234567890Wyx')
cursor = coon.cursor()

#数据规范化
cursor.execute("SELECT * FROM MRP")
data = cursor.fetchall()
col = cursor.description
length = len(col)
cols = [col[i][0] for i in range(length)]
df = pd.DataFrame([list(i) for i in data],columns=cols)
for i in df.index:
    df.loc[i,'父物料名称']=str(df.loc[i,'父物料名称']).strip()
    df.loc[i,'子物料名称']=str(df.loc[i,'子物料名称']).strip()
    df.loc[i,'调配方式']=str(df.loc[i,'调配方式']).strip()

#日期处理
def date_process(date,advance):
    start_date = dt.datetime.strptime(date,'%Y-%m-%d')
    start_date = start_date-dt.timedelta(days=advance)
    start_date = str(start_date.strftime("%Y-%m-%d"))
    return start_date

mat_list = []
mat_column = ['子物料名称','调配方式','需求数','开始日期','结束日期']

#MRP(不算仓库)
def material(mat,end_date,num):
    for i in df.index:
        if(df.loc[i,'父物料名称']==mat):
            mul = df.loc[i,'构成数']
            loss = df.loc[i,'损耗率']
            require = math.ceil(num * mul / (1 - loss))
            advance = int(df.loc[i,'作业提前期']+df.loc[i,'配料提前期']+df.loc[i,'供应商提前期'])
            start_date = date_process(end_date,advance)
            mat_list.append([df.loc[i,'子物料名称'],df.loc[i,'调配方式'],require,start_date,date_process(end_date,0)])
            material(df.loc[i,'子物料名称'],start_date,require)
    return

material('眼镜','2022-5-29',100)
print(mat_list)





'''
#GUI
top = tk.Tk()
top.mainloop()
'''
