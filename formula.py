import pyodbc
import pandas as pd
import datetime as dt
from tkinter import *
import math
from tkinter import messagebox
from tkinter import ttk

#数据库连接
coon = pyodbc.connect('DRIVER={SQL Server};SERVER=Z1020;DATABASE=MRP;UID=sa;PWD=1')
cursor = coon.cursor()
#数据规范化
cursor.execute("SELECT * FROM formula")
data = cursor.fetchall()
col = cursor.description
length = len(col)
cols = [col[i][0] for i in range(length)]
df = pd.DataFrame([list(i) for i in data],columns=cols)

for i in df.index:
    if (pd.isna(df.loc[i,'资产类汇总序号'])):
        df.loc[i, '资产类汇总序号']=-1
    df.loc[i, '变量名'] = str(df.loc[i, '变量名']).strip()
formu=[]
global count
def search(name):
    for i in df.index:
        if (df.loc[i,'变量名']==name):
            count =df.loc[i,'序号']
    for i in df.index:
        if(int(df.loc[i,'资产类汇总序号'])==count):
            formu.append(df.loc[i,'变量名'])

search('b3')
print(formu)