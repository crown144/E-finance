#数据库连接import pyodbc
import tkinter

import pandas as pd
import datetime as dt
from tkinter import *
import math
from tkinter import messagebox
from tkinter import ttk
import pyodbc

coon = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-RUINCH06;DATABASE=MRP;UID=sa;PWD=jiangwen123123')
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
cursor.execute("select 子物料名称,sum(工序库存+资材库存) as 库存 from MRP group by 子物料名称")
data = cursor.fetchall()
col = cursor.description
length = len(col)
cols = [col[i][0] for i in range(length)]
warehouse = pd.DataFrame([list(i) for i in data],columns=cols)
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

def transfer(date):
    return dt.datetime.strptime(date,'%Y-%m-%d').timestamp()




#GUI
top = Tk()
top.title('MRP计算')
top.geometry('+650+120')
# background_image = top.PhotoImage(file='R-C.png')
# background_label = Label(top, image=background_image)
# background_label.place(relwidth=1, relheight=1)
canvas = Canvas(top, height=700, width=400)
canvas.pack()

label1 = Label(top,text='物料名称',font=('微软雅黑',14))
label1.place(relx=0.2, rely=0.01, relwidth=0.2, relheight=0.05, anchor='n')
label2 = Label(top,text='需求数',font=('微软雅黑',14))
label2.place(relx=0.48,rely=0.01,relwidth=0.2, relheight=0.05, anchor='n')
label2 = Label(top,text='日期',font=('微软雅黑',14))
label2.place(relx=0.78,rely=0.01,relwidth=0.2, relheight=0.05, anchor='n')


txt1 = Entry(top,font=14,validate="focusout")
txt1.place(relx=0.09,rely=0.05,relwidth=0.22, relheight=0.05)
txt2 = Entry(top,font=14,validate="focusout")
txt2.place(relx=0.38,rely=0.05,relwidth=0.22, relheight=0.05)
txt3 = Entry(top,font=14 ,validate="focusout")
txt3.place(relx=0.66,rely=0.05,relwidth=0.28, relheight=0.05)


def callback():
    if txt1.get() == "" or txt2.get() == "" or txt3.get() == "":
        messagebox.showwarning("输入不正确")
    else :
        global str1,epoch,str3
        str1 = txt1.get()
        epoch = int(txt2.get())
        str3 = txt3.get()
    for i in df.index:
        if(df.loc[i,'子物料名称']==str1):
            global mat_list
            loss = df.loc[i,'损耗率']
            require = math.ceil(epoch / (1 - loss))
            advance = int(df.loc[i,'作业提前期']+df.loc[i,'配料提前期']+df.loc[i,'供应商提前期'])
            start_date = date_process(str3,advance)
            material(str1,start_date,epoch)
            require = update_num(i,require)
            mat_list.append([df.loc[i,'子物料名称'],df.loc[i,'调配方式'],require,start_date,date_process(str3,0)])
    mat_list = sorted(mat_list,key=lambda x:transfer(x[4]),reverse=TRUE)
    xscroll = Scrollbar(top, orient=HORIZONTAL)
    yscroll = Scrollbar(top, orient=VERTICAL)
    xscroll.pack(side=BOTTOM, fill=X)
    yscroll.pack(side=RIGHT, fill=Y)
    top.table = ttk.Treeview(
        master = top,
        columns = mat_column,
        height= 30,
        style= 'Treeview',
        xscrollcommand=xscroll.set,     # x轴滚动条
        yscrollcommand=yscroll.set
   )
    xscroll.config(command=top.table.xview)
    yscroll.config(command=top.table.yview)
    top.table.place(relx=0.09,rely=0.15,relwidth=0.8,relheight=0.7)  # TreeView加入frame
    for i in range(len(mat_column)):
        top.table.heading(column=mat_column[i], text=mat_column[i], anchor=CENTER,command=lambda: print(mat_column[i]))  # 设置除#0列以外的表头
        top.table.column(mat_column[i], minwidth=60, anchor=CENTER, stretch=True)  # 设置列

    print(mat_column)
    style = ttk.Style(top)
    style.configure('Treeview', rowheight=40)
    for data in mat_list:
        print(data)
        top.table.insert('', 'end' , text="", value=data)


def selection(self, event):
    # selection()方法可获取item或items
    print('选择的是：' + str(event.widget.selection()))  # event.widget获取Treeview对象
    return "break"

def pro_string(a):
    string = ""
    string += a
    string += '='
    string += formu[0]
    for i in formu:
        string += '+'
        string += i
    return string

def callback3(top2,txt4_value):
    print("txt4_value:", txt4_value)
    search(txt4_value)
    string = pro_string(txt4_value)
    print(string)
    txt = Text(top2)
    txt.delete("1.0",tkinter.END)
    txt.insert(tkinter.END,string)
    txt.place(relx = 0.1,rely= 0.2,relwidth= 0.70, relheight=0.05)

    print("callback3 called")

def on_confirm(top2,txt4_value):
    callback3(top2, txt4_value)

def callback2(top):
    top.destroy()
    top2 = Tk()
    top2.title('公式计算')
    top2.geometry('500x700+650+120')
    top2.focus_force()
    label4 = Label(top2, text='变量名称', font=('微软雅黑', 14))
    label4.place(relx=0.2, rely=0.05, relwidth=0.5, relheight=0.05, anchor='n')
    txt4 = Entry(top2, font=14, validate="focusout")
    txt4.place(relx=0.09, rely=0.1, relwidth=0.30, relheight=0.05)
    d =  Button(top2, text="确定",font=('微软雅黑',14), command=lambda :on_confirm(top2,txt4.get()))
    d.place(relx = 0.45,rely= 0.1,relwidth= 0.30, relheight=0.05)
    top2.mainloop()




# 使用按钮控件调用函数
b = Button(top, text="确定",font=('微软雅黑',14), command=callback)
c = Button(top, text="公式表计算",font=('微软雅黑',14),command=lambda :callback2(top))

b.place(relx = 0.25,rely= 0.15,relwidth= 0.30, relheight=0.07)
c.place(relx = 0.65,rely= 0.15,relwidth= 0.30, relheight=0.07)
top.mainloop()
cursor = coon.cursor()
#数据规范化
cursor.execute("SELECT * FROM formula")
data = cursor.fetchall()
col = cursor.description
length = len(col)
cols = [col[i][0] for i in range(length)]
df = pd.DataFrame([list(i) for i in data],columns=cols)
