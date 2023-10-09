import pyodbc
import pandas as pd
import datetime as dt
from tkinter import *
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

#计算库存
cursor.execute("select 子物料名称,sum(工序库存+资产库存) as 库存 from MRP group by 子物料名称")
data = cursor.fetchall()
col = cursor.description
length = len(col)
cols = [col[i][0] for i in range(length)]
warehouse = pd.DataFrame([list(i) for i in data],columns=cols)
for i in warehouse.index:
    warehouse.loc[i,'子物料名称']=str(warehouse.loc[i,'子物料名称']).strip()

#库存更新
def update_num(index,require):
    for j in warehouse.index:
        if(warehouse.loc[j,'子物料名称']==df.loc[index,'子物料名称']):
            n = warehouse.loc[j,'库存']
            warehouse.loc[j,'库存'] = warehouse.loc[j,'库存'] - n
            return require-n

#日期处理
def date_process(date,advance):
    start_date = dt.datetime.strptime(date,'%Y-%m-%d')
    start_date = start_date-dt.timedelta(days=advance)
    start_date = str(start_date.strftime("%Y-%m-%d"))
    return start_date

mat_list = []
mat_column = ['子物料名称','调配方式','需求数','开始日期','结束日期']

#MRP
def material(mat,end_date,num):
    for i in df.index:
        if(df.loc[i,'父物料名称']==mat):
            mul = df.loc[i,'构成数']
            loss = df.loc[i,'损耗率']
            require = math.ceil(num * mul / (1 - loss))
            advance = int(df.loc[i,'作业提前期']+df.loc[i,'配料提前期']+df.loc[i,'供应商提前期'])
            start_date = date_process(end_date,advance)
            material(df.loc[i,'子物料名称'],start_date,require)
            require = update_num(i,require)
            mat_list.append([df.loc[i,'子物料名称'],df.loc[i,'调配方式'],require,start_date,date_process(end_date,0)])
    return

material('眼镜','2022-5-29',100)
#print(mat_list)






#GUI
top = Tk()
top.title('MRP计算')
top.geometry('400x700+650+120')
lb = Label(top,text='neirong')
lb.grid(column=1,row=1)
lb = Label(top,text='neirong')
lb.grid(column=1,row=2)
lb = Label(top,text='neirong')
lb.grid(column=1,row=3)
txt = Entry(top)
txt.grid(column=2,row=2,ipady=4)
print(txt.grid_info())
top.mainloop()
