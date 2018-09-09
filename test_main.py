# -*- coding: utf-8 -*-
import xlrd
import xlwt
from datetime import date, datetime,timedelta
import pandas as pd
from pandas import DataFrame
import sqlalchemy
import seaborn as sns
from scipy import stats

import logging
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pylab import mpl
import matplotlib.font_manager as fm
fonts = fm.FontProperties(fname='C:\Windows\Fonts\STXINWEI.TTF',size=16) # 设置字体
# # sns.set(font=fonts.get_name())
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# sns.set(font='SimHei')



def str2float(str):
    return float(str)

def testFit():
    pass
    # kde = stats.gaussian_kde()

# 打印日志
def printLog(str):
    # 创建Logger
    logger = logging.getLogger("logToScreen")
    logger.setLevel(logging.DEBUG)

    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)

    # 添加到Logger中
    logger.addHandler(consoleHandler)

    # 打印日志
    # logger.debug('debug 信息')
    # logger.info('info 信息')
    logger.warning('警告：文件%s中存在空值，请稍后处理：' % str)
    # logger.error('error 信息')
    # logger.critical('critical 信息')
    # logger.debug('%s 是自定义信息' % '这些东西')

# 去除数据指定列中的异常值
def RemoveErrVal(data,keyword,errValue):
    for key in keyword:
        for err in errValue:
            # 去除异常值
            try:
                data = data[(data[key] != err)]
            except TypeError as e:
                print("该组数据可能没有字符串类型，默认float：",e)
                print(data.dtypes)
                continue
    return data

# 查看数据集是否存在数据为NULL的列
def checkIsNull(df,str):
    # pass
    allColumns = df.isnull().any()
    for i in range(len(allColumns)):
        if allColumns[i]:
            printLog(str)
            return


# matplotlib画图简用
def print_plot(data, keyword,title='', xlab='', ylab='',bins=10):
    global fonts
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(data[keyword], bins=50)
    plt.title(title, fontproperties=fonts)
    plt.xlabel(xlab, fontproperties=fonts)
    plt.ylabel(ylab, fontproperties=fonts)
    plt.show()

# 使用seaborn的distplot功能绘制同类数据的概率密度分布对比情况
def print_plot_sns_compare(data,keyword, title='', xlab='', ylab='',bins=[]):
    sns.set(palette="muted", color_codes=True,font='SimHei')
    length = len(data)
    f, axes = plt.subplots(1, length, figsize=(21, 7))
    for i in range(length):
        sns.distplot(data[i][keyword[i]], bins=bins[i], kde_kws={"shade": True, "color":"g"}, hist_kws={"color":"b"}#,fit=stats.gausshyper
                     , ax=axes[i])
    plt.show()


# 使用seaborn的distplot功能绘制三组不同类别数据分布的概率密度曲线、直方图和fit拟合情况
def print_plot_sns_2(data,keyword,dataAnother='',keywordAnother=[], isTrain=True,title='', xlab='', ylab='',bins=10,binsAnother=10):
    sns.set(palette="muted", color_codes=True,font='SimHei')
    # length = len(keyword)
    # if keywordAnother is not None:
    #     length = length+1
    if isTrain:
        row = 1
    else:
        row = 2
    f, axes = plt.subplots(row, 3, figsize=(21, 7))
    if isTrain:
        sns.distplot(data[keyword[0]], bins=bins, isTrain=isTrain, kde_kws={"shade": True, "color":"g"}, hist_kws={"color":"b"},fit=stats.lognorm
                     , ax=axes[0])
        sns.distplot(data[keyword[1]], bins=15, isTrain=isTrain, kde_kws={"shade": True, "color": "g"}, hist_kws={"color": "b"},fit=stats.dgaussian
                     , ax=axes[1])
        if keywordAnother is not None:
            sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,  kde_kws={"shade": True, "color": "g"},fit=stats.lognorm
                     , hist_kws={"color": "b"}, ax=axes[2])
    else:
        sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
                     kde_kws={"shade": True, "color": "g", "label": "johnsonsb"}, hist_kws={"color": "b"},  fit=stats.johnsonsb,
                     kernelParam=(1.4325670652903717, 1.0348251160259663, 17.211478681707643, 112.41785769036785),
                     ax=axes[0,0])
        sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
                     kde_kws={"shade": True, "color": "g", "label": "johnsonsu"}, hist_kws={"color": "b"},  fit=stats.johnsonsu,
                     kernelParam=(-7.4499423241262814, 1.8585724577861038, 10.957566210490761, 1.0402938745385364),
                     ax=axes[0,1])
        # sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
        #              kde_kws={"shade": True, "color": "g", "label": "rice"}, hist_kws={"color": "b"},  fit=stats.rice,
        #              kernelParam=(0.00030771725667398447, 14.5717118769265, 24.029115689191158),
        #              ax=axes[0,2])
        # sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
        #              kde_kws={"shade": True, "color": "g", "label": "invgamma"}, hist_kws={"color": "b"}, fit=stats.invgamma,
        #              kernelParam=(7.8329924522526717, -1.7298211131927927, 312.80357615655112), ax=axes[1,0])
        # sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
        #              kde_kws={"shade": True, "color": "g", "label": "invgauss"}, hist_kws={"color": "b"},
        #              fit=stats.invgauss,
        #              kernelParam=(0.30642986141359135, 10.136428671414453, 110.07424236342952),
        #              ax=axes[1,1])
        # sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain,
        #              kde_kws={"shade": True, "color": "g", "label": "invweibull"}, hist_kws={"color": "b"},
        #              fit=stats.invweibull,
        #              kernelParam=(11.892095445918237, -115.11585487508093, 150.56184348200534),
        #              ax=axes[1,2])


        # if keywordAnother is not None:
        #     sns.distplot(dataAnother[keywordAnother[0]], bins=binsAnother, isTrain=isTrain, kde_kws={"shade": True, "color": "g"}, hist_kws={"color": "b"},#fit=stats.lognorm,
        #                  kernelParam=(0.53581011274768198, 10.824696055450907, 28.800524079608266), ax=axes[2])

    plt.show()

# 使用seaborn的distplot功能绘制两组不同类别数据分布的概率密度曲线、直方图分布情况
def print_plot_sns(data, keyword, title='', xlab='', ylab='', bins=10):
    sns.set(palette="muted", color_codes=True)
    f, axes = plt.subplots(1, 2, figsize=(10, 10))
    sns.distplot(data[keyword[0]], bins=bins, kde_kws={"shade": True, "color": "g"}, hist_kws={"color": "b"},
                 ax=axes[0])
    sns.distplot(data[keyword[1]], bins=30, kde_kws={"shade": True, "color": "g"}, hist_kws={"color": "b"},
                 ax=axes[1])
    plt.show()


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(r'F:\轮胎项目\导出数据\接口2数据2列表_203_6.15-6.30尾\接口2数据2列表_203_6.15-6.16.xlsx')
    # 获取所有sheet
    print(workbook.sheet_names())  # [u'sheet1', u'sheet2']
    sheet2_name = workbook.sheet_names()[0]

    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0)

    # sheet的名称，行数，列数
    print(sheet.name, sheet.nrows, sheet.ncols,type(sheet))

    # 获取整行和整列的值（数组）
    rows = sheet.row_values(3)  # 获取第四行内容
    cols = sheet.col_values(11)  # 获取第三列内容
    cols1 = sheet.col_values(10)  # 获取第三列内容
    cols25 = sheet.col_values(25)  # 获取第三列内容

    # print(cols.ctype,cols)
    # for index in range(len(rows)):
    #     print(rows[index],type(rows[index]))
    print(rows)
    print(cols,'\n',type(cols[0]))

    # # 将字符串型的列表元素转换成数字类型列表（float、int等）
    # cols = list(map(eval,cols[1:]))
    # cols1 = list(map(eval,cols1[1:]))
    # cols25 = list(map(eval,cols25[1:]))
    # print(cols,'\n',type(cols[0]))
    # print(cols1,'\n',type(cols1),type(cols1[0]),'\n',sorted(cols1))
    # print(cols25, '\n', type(cols25), type(cols25[0]), '\n', sorted(cols25))

    # # 获取单元格内容
    # print(sheet.cell(1, 0).value)
    # print(sheet.cell_value(1, 0))
    # print(sheet.row(1)[0].value)
    #
    # # 获取单元格内容的数据类型
    # # ctype: 0 empty, 1 string, 2 number, 3 date, 4 boolean, 5 error
    # print(sheet.cell(1, 0).ctype)


def read_excel_wtpd():
    # pass
    oraengine = sqlalchemy.create_engine('oracle://TireProject:jl123456@localhost:1521/orcl')


    # # for 接口2数据2列表_203
    # file_name = ['接口2数据2列表_203_6.15-6.16.xlsx', '接口2数据2列表_203_6.16-6.17.xlsx', '接口2数据2列表_203_6.17-6.18.xlsx',
    #              '接口2数据2列表_203_6.18-6.20.xlsx', '接口2数据2列表_203_6.20-6.21.xlsx', '接口2数据2列表_203_6.21-6.23.xlsx',
    #              '接口2数据2列表_203_6.23-6.24.xlsx', '接口2数据2列表_203_6.27-6.28.xlsx', '接口2数据2列表_203_6.28-6.29.xlsx',
    #              '接口2数据2列表_203_6.29-6.30.xlsx']
    # file_name = ['接口2数据2列表_203_5.25-6.5.xlsx', '接口2数据2列表_203_6.5-6.9.xlsx', '接口2数据2列表_203_6.9-6.15.xlsx']


    # for 接口2数据2列表_207
    # file_name = ['接口2数据2列表_207_6.20-6.21.xlsx', '接口2数据2列表_207_6.21-6.22.xlsx', '接口2数据2列表_207_6.22-6.23.xlsx',
    #              '接口2数据2列表_207_6.23-6.24.xlsx', '接口2数据2列表_207_6.24-6.25.xlsx', '接口2数据2列表_207_6.25-6.26.xlsx',
    #              '接口2数据2列表_207_6.26-6.27.xlsx', '接口2数据2列表_207_6.27-6.28.xlsx', '接口2数据2列表_207_6.28-6.29.xlsx',
    #              '接口2数据2列表_207_6.29-6.30尾.xlsx']
    # file_name = ['接口2数据2列表_207_5.15-6.15.xlsx']


    # # for 接口2数据2列表_208
    # file_name = ['接口2数据2列表_208_6.15-6.16.xlsx', '接口2数据2列表_208_6.16-6.17.xlsx', '接口2数据2列表_208_6.17-6.18.xlsx',
    #              '接口2数据2列表_208_6.18-6.19.xlsx', '接口2数据2列表_208_6.19-6.20.xlsx', '接口2数据2列表_208_6.20-6.21.xlsx',
    #              '接口2数据2列表_208_6.23-6.24.xlsx', '接口2数据2列表_208_6.24-6.25.xlsx', '接口2数据2列表_208_6.25-6.26.xlsx',
    #              '接口2数据2列表_208_6.26-6.27.xlsx', '接口2数据2列表_208_6.27-6.28.xlsx', '接口2数据2列表_208_6.28-6.29.xlsx',
    #              '接口2数据2列表_208_6.29-6.30.xlsx', '接口2数据2列表_208_6.30-6.30尾.xlsx']
    # file_name = ['接口2数据2列表_208_5.15-6.1.xlsx','接口2数据2列表_208_6.1-6.5.xlsx','接口2数据2列表_208_6.5-6.15.xlsx']

    # # for 接口2数据2列表_测试集
    # file_name = ['接口2数据2列表_203_7.1-7.12.xlsx', '接口2数据2列表_203_7.13-7.15.xlsx', '接口2数据2列表_207_7.1.xlsx',
    #              '接口2数据2列表_207_7.2.xlsx',      '接口2数据2列表_207_7.3.xlsx',       '接口2数据2列表_207_7.4.xlsx',
    #              '接口2数据2列表_207_7.5.xlsx',      '接口2数据2列表_207_7.6.xlsx',       '接口2数据2列表_207_7.7.xlsx',
    #              '接口2数据2列表_207_7.8-7.12.xlsx', '接口2数据2列表_207_7.13-7.15.xlsx', '接口2数据2列表_208_7.1-7.4.xlsx',
    #              '接口2数据2列表_208_7.5-7.12.xlsx', '接口2数据2列表_208_7.13-7.15.xlsx' ]



    # # # for 接口1数据列表_203
    # # file_name = ['接口1数据列表_203_6.15-6.16.xlsx', '接口1数据列表_203_6.16-6.17.xlsx', '接口1数据列表_203_6.17-6.18.xlsx',
    # #          '接口1数据列表_203_6.18-6.20.xlsx', '接口1数据列表_203_6.20-6.21.xlsx', '接口1数据列表_203_6.21-6.23.xlsx',
    # #          '接口1数据列表_203_6.23-6.26.xlsx', '接口1数据列表_203_6.26-6.29.xlsx','接口1数据列表_203_6.29-6.30尾.xlsx'  ]
    # file_name = ['接口1数据列表_203_6.12-6.15.xlsx', '接口1数据列表_203_6.10-6.12.xlsx','接口1数据列表_203_6.9-6.10.xlsx',
    #              '接口1数据列表_203_6.8-6.9.xlsx','接口1数据列表_203_5.25-6.8.xlsx']

    # # # for 接口1数据列表_207
    # # file_name = ['接口1数据列表_207_6.20-6.22.xlsx', '接口1数据列表_207_6.22-6.24.xlsx',
    # #          '接口1数据列表_207_6.24-6.26.xlsx', '接口1数据列表_207_6.26-6.28.xlsx','接口1数据列表_207_6.28-6.30尾.xlsx'  ]
    # file_name = ['接口1数据列表_207_5.25-6.15.xlsx']

    # # # # for 接口1数据列表_208
    # # file_name = ['接口1数据列表_208_6.15-6.18.xlsx', '接口1数据列表_208_6.18-6.20.xlsx',
    # #          '接口1数据列表_208_6.20-6.22.xlsx', '接口1数据列表_208_6.22-6.24.xlsx', '接口1数据列表_208_6.24-6.26.xlsx',
    # #          '接口1数据列表_208_6.26-6.28.xlsx', '接口1数据列表_208_6.28-6.30.xlsx','接口1数据列表_208_6.30-6.30尾.xlsx'  ]
    # file_name = ['接口1数据列表_208_5.25-6.10.xlsx', '接口1数据列表_208_6.10-6.15.xlsx']

    # # # for 接口1数据列表_测试集
    # file_name = ['接口1数据列表_203_7.1-7.12.xlsx', '接口1数据列表_203_7.13-7.15.xlsx', '接口1数据列表_207_7.1.xlsx',     '接口1数据列表_207_7.2.xlsx',
    #              '接口1数据列表_207_7.3.xlsx',
    #              '接口1数据列表_207_7.4.xlsx',      '接口1数据列表_207_7.5.xlsx',       '接口1数据列表_207_7.6.xlsx',     '接口1数据列表_207_7.7.xlsx',
    #              '接口1数据列表_207_7.8.xlsx',      '接口1数据列表_207_7.9.xlsx',       '接口1数据列表_207_7.10.xlsx',    '接口1数据列表_207_7.11.xlsx',
    #              '接口1数据列表_207_7.12.xlsx',     '接口1数据列表_207_7.13-7.15.xlsx', '接口1数据列表_208_7.1.xlsx',     '接口1数据列表_208_7.2.xlsx',
    #              '接口1数据列表_208_7.3.xlsx',      '接口1数据列表_208_7.4.xlsx',       '接口1数据列表_208_7.5.xlsx',
    #              '接口1数据列表_208_7.6.xlsx'       '接口1数据列表_208_7.7.xlsx',       '接口1数据列表_208_7.8-7.9.xlsx', '接口1数据列表_208_7.10.xlsx',
    #              '接口1数据列表_208_7.11.xlsx',     '接口1数据列表_208_7.12.xlsx',      '接口1数据列表_208_7.13-7.15.xlsx' ]
    # file_name = ['接口1数据列表_208_7.6.xlsx' ,      '接口1数据列表_208_7.7.xlsx',       '接口1数据列表_208_7.8-7.9.xlsx', '接口1数据列表_208_7.10.xlsx',
    #              '接口1数据列表_208_7.11.xlsx',     '接口1数据列表_208_7.12.xlsx',      '接口1数据列表_208_7.13-7.15.xlsx' ]



    # # # # for 其他数据列表_203
    # file_name = ['其他数据列表_203_6.15-6.22.xlsx', '其他数据列表_203_6.22-6.23.xlsx','其他数据列表_203_6.23-6.24.xlsx',
    #              '其他数据列表_203_6.27-6.28.xlsx', '其他数据列表_203_6.28-6.29.xlsx','其他数据列表_203_6.29-6.30尾.xlsx'  ]
    # file_name = ['其他数据列表_203_5.25-6.15.xlsx']


    # # # for 其他数据列表_207
    # file_name = ['其他数据列表_207_6.20-6.26.xlsx', '其他数据列表_207_6.26-6.27.xlsx', '其他数据列表_207_6.27-6.28.xlsx',
    #              '其他数据列表_207_6.28-6.29.xlsx', '其他数据列表_207_6.29-6.30尾.xlsx']
    # file_name = ['其他数据列表_207_5.25-6.15.xlsx']


    # # # # for 其他数据列表_208
    # file_name = ['其他数据列表_208_6.15-6.22.xlsx', '其他数据列表_208_6.23-6.24.xlsx', '其他数据列表_208_6.24-6.25.xlsx',
    #              '其他数据列表_208_6.25-6.26.xlsx', '其他数据列表_208_6.26-6.27.xlsx', '其他数据列表_208_6.27-6.28.xlsx',
    #              '其他数据列表_208_6.28-6.29.xlsx', '其他数据列表_208_6.29-6.30尾.xlsx'  ]
    # file_name = ['其他数据列表_208_5.15-6.15.xlsx']

    # # # for 其他数据列表_测试集
    file_name = ['其他数据列表_203_7.1-7.12.xlsx', '其他数据列表_203_7.13-7.15.xlsx', '其他数据列表_207_7.1-7.12.xlsx',
                 '其他数据列表_207_7.13-7.15.xlsx', '其他数据列表_208_7.1-7.12.xlsx', '其他数据列表_208_7.13-7.15.xlsx']




    for str in file_name:
        excel = pd.read_excel(r'F:\轮胎项目\导出数据\其他数据列表_训练数据\\' + str)
        print(excel,excel.values,'\n',type(excel),'\n',type(excel.values))
        print(excel.columns,'\n',excel.index)
        # print(excel["C5信号丢失报警"])
        print(excel.dtypes)

        checkIsNull(excel,str)

        print('--------------分割线-------------')

        excel.loc[:,["终端设备时间","平台接收时间"]] = excel.loc[:,["终端设备时间","平台接收时间"]].apply(pd.to_datetime)
        print(excel)
        print(excel.dtypes)
        print(excel.__len__())
        excel.to_sql('其他数据列表_测试集', oraengine, if_exists="append", index=False, chunksize=100)

    # excel_no_lost = excel.loc[excel["C5信号丢失报警"].isin(["C5-已报警"])]
    # # excel_no_lost = excel
    #
    # print(excel_no_lost)
    # print(excel_no_lost.dtypes)
    #
    # print('--------------分割线-------------')

    # excel_no_lost.loc[:,["终端设备时间","平台接收时间"]] = excel_no_lost.loc[:,["终端设备时间","平台接收时间"]].apply(pd.to_datetime)
    # # excel_no_lost.loc[:, ["终端设备时间", "平台接收时间"]].apply(pd.to_datetime)
    # print(excel_no_lost)
    # print(excel_no_lost.dtypes)


def test():
    oraengine = sqlalchemy.create_engine('oracle://TireProject:jl123456@localhost:1521/orcl')
    # data = pd.DataFrame([[1,2,3],[4,5,6],[77,8,9],[10,11,12]],columns=['col1','col2','col3'])

    # Data For DB
    # data = pd.read_sql('select * from test1',oraengine)
    # print(data)
    # checkIsNull(data,'test')
    # data.to_sql("test1",oraengine,if_exists="replace",index=True,chunksize=3000,index_label=['nihao'])

    # Data For Excel
    # excel = pd.read_excel(r'F:\轮胎项目\导出数据\接口1数据列表_203_6.15-6.30尾部\接口1数据列表_203_6.15-6.16.xlsx')
    # print(excel)
    # print(excel.dtypes)
    # print(excel)
    # excel.loc[:, ["终端设备时间", "平台接收时间"]] = excel.loc[:, ["终端设备时间", "平台接收时间"]].apply(pd.to_datetime)

    # excel.to_sql('接口1数据_TEST1',oraengine,if_exists="append",index=False,chunksize=100)




def read_excel_threshold():
    oraengine = sqlalchemy.create_engine('oracle://TireProject:jl123456@localhost:1521/orcl')

# # 拟合训练
# #
    file_directory = 'F:\轮胎项目\导出数据\整合(5.25-6.30)\\'

    excel_name1_g = '毂温数据_203(5.25-6.30).xlsx'
    excel_name2_g = '毂温数据_207(5.25-6.30).xlsx'
    excel_name3_g = '毂温数据_208(5.15-6.30).xlsx'
    excel1_g = pd.read_excel(file_directory + excel_name1_g)
    excel2_g = pd.read_excel(file_directory + excel_name2_g)
    excel3_g = pd.read_excel(file_directory + excel_name3_g)

    excel_g = pd.concat([excel1_g[["数据（℃）"]], excel2_g[["数据（℃）"]], excel3_g[["数据（℃）"]]])

    # 考虑去除毂温数据集的特殊值和边界值
    data_g = RemoveErrVal(excel_g, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    data_g.loc[:, ["数据（℃）"]] = data_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    # data_g = data_g[(data_g["数据（℃）"] > 5) & (data_g["数据（℃）"] < 120)]
    data_g = data_g[(data_g["数据（℃）"] > 0)]

    print(data_g[["数据（℃）"]].describe())
    print("毂温数据偏度：", data_g["数据（℃）"].skew())
    print('----------------分割线-------------------')
    # print_plot_sns(data_g, keyword=["数据（℃）"], title='轮胎监测系统', xlab='胎压', ylab='概率密度', bins=20)


    # excel for 绑带式轮胎温度203
    excel_name1 = '绑带式轮胎数据_203(5.25-6.30).xlsx'
    excel_name2 = '绑带式轮胎数据_207(5.25-6.30).xlsx'
    excel_name3 = '绑带式轮胎数据_208(5.15-6.30).xlsx'
    excel1 = pd.read_excel(file_directory + excel_name1)
    excel2 = pd.read_excel(file_directory + excel_name2)
    excel3 = pd.read_excel(file_directory + excel_name3)
    excel = pd.concat([excel1[["轮胎温度（℃）","轮胎压力（Bar）"]],excel2[["轮胎温度（℃）","轮胎压力（Bar）"]],excel3[["轮胎温度（℃）","轮胎压力（Bar）"]]])

    ## 去除轮胎数据集异常值和边界值
    data = RemoveErrVal(excel,keyword=["轮胎温度（℃）","轮胎压力（Bar）"],errValue=['无','-1.04','-50'])
    data.loc[:, ["轮胎温度（℃）","轮胎压力（Bar）"]] = data.loc[:, ["轮胎温度（℃）","轮胎压力（Bar）"]].apply(pd.to_numeric)
    # data = data[(data["轮胎温度（℃）"] > 5) & (data["轮胎压力（Bar）"] > 4) & (data["轮胎温度（℃）"] < 100)]
    data = data[(data["轮胎温度（℃）"] > 0) & (data["轮胎压力（Bar）"] > 0)]

    print(data[["轮胎温度（℃）", "轮胎压力（Bar）"]].describe())
    print("轮胎温度偏度：", data["轮胎温度（℃）"].skew(), "轮胎压力偏度：", data["轮胎压力（Bar）"].skew())

    # # 数据展示
    # print_plot_sns_2(data,isTrain=False,keyword=["轮胎温度（℃）","轮胎压力（Bar）"], dataAnother=data_g,keywordAnother=["数据（℃）"],
    #                  title='轮胎监测系统',xlab='胎压', ylab='概率密度' ,bins=20, binsAnother=30)
    print_plot_sns_2(data,isTrain=True,keyword=["轮胎温度（℃）","轮胎压力（Bar）"], dataAnother=data_g,keywordAnother=["数据（℃）"],
                     title='轮胎监测系统',xlab='胎压', ylab='概率密度' ,bins=25, binsAnother=35)

#     根据经验值，统计各经验阈值在训练集中所占的比例
    print('训练集个经验阈值在样本中体重所占比例：')
    print('毂温高温预警阈值130℃所占比例：',len(data_g[data_g["数据（℃）"] >= 130]) * 1.0 / len(data_g))
    print('毂温高温报警阈值180℃所占比例：',len(data_g[data_g["数据（℃）"] >= 180]) * 1.0 / len(data_g))
    print('轮胎高温报警阈值85℃所占比例：',len(data[data["轮胎温度（℃）"] >= 85]) * 1.0 / len(data))
    print('轮胎高压预警阈值10.5 Bar所占比例：',len(data[data["轮胎压力（Bar）"] >= 10.5]) * 1.0 / len(data))
    print('轮胎高压报警阈值10.94 Bar所占比例：',len(data[data["轮胎压力（Bar）"] >= 10.94]) * 1.0 / len(data))
    print('轮胎低压预警阈值7.44 Bar所占比例：',len(data[data["轮胎压力（Bar）"] <= 7.44]) * 1.0 / len(data))




# # # 拟合测试验证
#     file_directory = 'F:\轮胎项目\导出数据\整合测试集(7.1-7.15)\\'
#
#     excel_guwen = '毂温测试数据集.xlsx'
#     excel_luntai = '胎压胎温测试数据集.xlsx'
#
#     data_guwen = pd.read_excel(file_directory + excel_guwen,usecols=[12])
#     data_luntai = pd.read_excel(file_directory + excel_luntai,usecols=[10,11])
#
#     # 考虑去除特殊值和边界值
#     data_guwen = RemoveErrVal(data_guwen, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
#     data_guwen.loc[:, ["数据（℃）"]] = data_guwen.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
#     data_guwen = data_guwen[(data_guwen["数据（℃）"] > 5) & (data_guwen["数据（℃）"] < 120)]
#     print(data_guwen.describe())
#     print("毂温偏度：", data_guwen["数据（℃）"].skew())
#
#     data_luntai = RemoveErrVal(data_luntai,keyword=["轮胎温度（℃）","轮胎压力（Bar）"],errValue=['无','-1.04','-50'])
#     data_luntai.loc[:, ["轮胎温度（℃）","轮胎压力（Bar）"]] = data_luntai.loc[:, ["轮胎温度（℃）","轮胎压力（Bar）"]].apply(pd.to_numeric)
#     data_luntai = data_luntai[(data_luntai["轮胎温度（℃）"] > 5) & (data_luntai["轮胎压力（Bar）"] > 4) & (data_luntai["轮胎温度（℃）"] < 100)]
#     print(data_luntai[["轮胎温度（℃）", "轮胎压力（Bar）"]].describe())
#     print("轮胎温度偏度：", data_luntai["轮胎温度（℃）"].skew(), "轮胎压力偏度：", data_luntai["轮胎压力（Bar）"].skew())
#
#     print_plot_sns_2(data_luntai, isTrain=False, keyword=["轮胎温度（℃）","轮胎压力（Bar）"], dataAnother=data_guwen,keywordAnother=["数据（℃）"],
#                      title='轮胎监测系统',xlab='胎压', ylab='概率密度' ,bins=20, binsAnother=30)





def read_excel_threshold_compare():
    oraengine = sqlalchemy.create_engine('oracle://TireProject:jl123456@localhost:1521/orcl')


    # 拟合训练
    file_directory = 'F:\轮胎项目\导出数据\整合(5.25-6.30)\\'
    excel_name1_g = '毂温数据_203(5.25-6.30).xlsx'
    excel_name2_g = '毂温数据_207(5.25-6.30).xlsx'
    excel_name3_g = '毂温数据_208(5.15-6.30).xlsx'
    # excel_name1_g = '绑带式轮胎数据_203(5.25-6.30).xlsx'
    # excel_name2_g = '绑带式轮胎数据_207(5.25-6.30).xlsx'
    # excel_name3_g = '绑带式轮胎数据_208(5.15-6.30).xlsx'
    excel1_g = pd.read_excel(file_directory + excel_name1_g)
    excel2_g = pd.read_excel(file_directory + excel_name2_g)
    excel3_g = pd.read_excel(file_directory + excel_name3_g)
    # excel_g = pd.concat([excel1_g[["数据（℃）"]], excel2_g[["数据（℃）"]], excel3_g[["数据（℃）"]]])
    data1_g = RemoveErrVal(excel1_g, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    data2_g = RemoveErrVal(excel2_g, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    data3_g = RemoveErrVal(excel3_g, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])

    data1_g.loc[:, ["数据（℃）"]] = data1_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    data2_g.loc[:, ["数据（℃）"]] = data2_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    data3_g.loc[:, ["数据（℃）"]] = data3_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    # 考虑去除边界值
    data1_g = data1_g[(data1_g["数据（℃）"] > 5) & (data1_g["数据（℃）"] < 180)]
    data2_g = data2_g[(data2_g["数据（℃）"] > 5) & (data2_g["数据（℃）"] < 180)]
    data3_g = data3_g[(data3_g["数据（℃）"] > 5) & (data3_g["数据（℃）"] < 180)]

    print(data1_g[["数据（℃）"]].describe(),'\n',data2_g[["数据（℃）"]].describe(),'\n',data3_g[["数据（℃）"]].describe())
    print("轮毂温度偏度：", data1_g["数据（℃）"].skew(),data2_g["数据（℃）"].skew(),data2_g["数据（℃）"].skew())

    print_plot_sns_compare([data1_g,data2_g,data3_g],["数据（℃）","数据（℃）","数据（℃）"],bins=[30,30,30])


# 测试数据集

    file_directory_test = 'F:\轮胎项目\导出数据\整合测试集(7.1-7.15)\\'
    excel_luntai = '胎压胎温测试数据集.xlsx'
    excel_guwen = '毂温测试数据集.xlsx'

    data_guwen = pd.read_excel(file_directory_test + excel_guwen)
    data_luntai = pd.read_excel(file_directory_test + excel_luntai)

    # excel_g = pd.concat([excel1_g[["数据（℃）"]], excel2_g[["数据（℃）"]], excel3_g[["数据（℃）"]]])
    data1_g = RemoveErrVal(data_guwen[data_guwen["设备ID"] == 'zwgps180203'], keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    data2_g = RemoveErrVal(data_guwen[data_guwen["设备ID"] == 'zwgps180207'], keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    data3_g = RemoveErrVal(data_guwen[data_guwen["设备ID"] == 'zwgps180208'], keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])

    data1_g.loc[:, ["数据（℃）"]] = data1_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    data2_g.loc[:, ["数据（℃）"]] = data2_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    data3_g.loc[:, ["数据（℃）"]] = data3_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    # 考虑去除边界值
    data1_g = data1_g[(data1_g["数据（℃）"] > 3) & (data1_g["数据（℃）"] < 180)]
    data2_g = data2_g[(data2_g["数据（℃）"] > 3) & (data2_g["数据（℃）"] < 180)]
    data3_g = data3_g[(data3_g["数据（℃）"] > 3) & (data3_g["数据（℃）"] < 180)]

    print(data1_g[["数据（℃）"]].describe(),'\n',data2_g[["数据（℃）"]].describe(),'\n',data3_g[["数据（℃）"]].describe())
    print("轮毂温度偏度：", data1_g["数据（℃）"].skew(),data2_g["数据（℃）"].skew(),data2_g["数据（℃）"].skew())

    print_plot_sns_compare([data1_g,data2_g,data3_g],["数据（℃）","数据（℃）","数据（℃）"],bins=[30,30,30])




def read_excel_time_axis():
    file_directory = 'F:\轮胎项目\导出数据\整合(5.25-6.30)\\'

    excel_name1_g = '绑带式轮胎数据_203(5.25-6.30).xlsx'
    excel_name2_g = '绑带式轮胎数据_207(5.25-6.30).xlsx'
    excel_name3_g = '绑带式轮胎数据_208(5.15-6.30).xlsx'
    # excel_name1_g = '毂温数据_203(5.25-6.30).xlsx'
    # excel_name2_g = '毂温数据_207(5.25-6.30).xlsx'
    # excel_name3_g = '毂温数据_208(5.15-6.30).xlsx'


    # excel_name1_g = '胎压胎温测试数据集.xlsx'
    excel_name = excel_name3_g
    excel1_g = pd.read_excel(file_directory + excel_name)
    # excel1_g = excel1_g[excel1_g['设备ID'] == 'zwgps180207']


    # 时段筛选
    # # for 203
    # excel1_g.loc[:, ["终端设备时间", "平台接收时间"]] = excel1_g.loc[:, ["终端设备时间", "平台接收时间"]].apply(pd.to_datetime)
    # excel_g = excel1_g[(excel1_g["平台接收时间"] >= datetime.strptime('2018/6/1 00:00:00', '%Y/%m/%d %H:%M:%S'))
    #                    & (excel1_g["平台接收时间"] <= datetime.strptime('2018/6/15 00:00:00', '%Y/%m/%d %H:%M:%S'))
    #                    & (excel1_g["终端设备时间"] >= datetime.strptime('2018/5/30 05:00:00', '%Y/%m/%d %H:%M:%S'))]

    # for 207
    excel1_g.loc[:, ["终端设备时间", "平台接收时间"]] = excel1_g.loc[:, ["终端设备时间", "平台接收时间"]].apply(pd.to_datetime)
    excel_g = excel1_g[(excel1_g["平台接收时间"]>=datetime.strptime('2018/6/1 00:00:00','%Y/%m/%d %H:%M:%S'))
                       & (excel1_g["平台接收时间"]<=datetime.strptime('2018/6/11 00:00:00','%Y/%m/%d %H:%M:%S'))
                       &(excel1_g["终端设备时间"]>=datetime.strptime('2018/5/30 05:00:00','%Y/%m/%d %H:%M:%S')) ]

    # # for 208
    # excel1_g.loc[:, ["终端设备时间", "平台接收时间"]] = excel1_g.loc[:, ["终端设备时间", "平台接收时间"]].apply(pd.to_datetime)
    # excel_g = excel1_g[(excel1_g["平台接收时间"] >= datetime.strptime('2018/6/5 05:00:00', '%Y/%m/%d %H:%M:%S'))
    #                    & (excel1_g["平台接收时间"] <= datetime.strptime('2018/6/8 00:00:00', '%Y/%m/%d %H:%M:%S'))
    #                    & (excel1_g["终端设备时间"] >= datetime.strptime('2018/6/1 05:00:00', '%Y/%m/%d %H:%M:%S'))]





    data_g = RemoveErrVal(excel_g, keyword=["轮胎温度（℃）", "轮胎压力（Bar）"], errValue=['无', '-1.04', '-50'])
    data_g.loc[:, ["轮胎温度（℃）", "轮胎压力（Bar）"]] = data_g.loc[:, ["轮胎温度（℃）", "轮胎压力（Bar）"]].apply(pd.to_numeric)
    # data_g = RemoveErrVal(excel_g, keyword=["数据（℃）"], errValue=['无', '-1.04', '-50'])
    # data_g.loc[:, ["数据（℃）"]] = data_g.loc[:, ["数据（℃）"]].apply(pd.to_numeric)
    data_g = data_g[data_g["轮胎温度（℃）"]<150]

    # # 分车
    car0_data = data_g[data_g["车编号"] == 0]
    car1_data = data_g[data_g["车编号"] == 1]
    # 毂温
    # car1_data = data_g



    # 分轮胎
    # # 牵引车分轮胎（208车的牵引台0123，其他车均为8 9 10 11）
    luntai008_data = car0_data[car0_data["轮胎编号"] == 0]
    luntai009_data = car0_data[car0_data["轮胎编号"] == 1]
    luntai010_data = car0_data[car0_data["轮胎编号"] == 2]
    luntai011_data = car0_data[car0_data["轮胎编号"] == 3]
    # # 挂车分轮胎
    # luntai100_data = car1_data[car1_data["轮胎编号"] == 0]
    # luntai101_data = car1_data[car1_data["轮胎编号"] == 1]
    # luntai102_data = car1_data[car1_data["轮胎编号"] == 2]
    # luntai103_data = car1_data[car1_data["轮胎编号"] == 3]
    # luntai108_data = car1_data[car1_data["轮胎编号"] == 8]
    # luntai109_data = car1_data[car1_data["轮胎编号"] == 9]
    # luntai110_data = car1_data[car1_data["轮胎编号"] == 10]
    # luntai111_data = car1_data[car1_data["轮胎编号"] == 11]
    # for 毂温分轮胎
    # luntai100_data = car1_data[car1_data["顺序编号"] == 1]
    # luntai101_data = car1_data[car1_data["顺序编号"] == 2]
    # luntai102_data = car1_data[car1_data["顺序编号"] == 3]
    # luntai103_data = car1_data[car1_data["顺序编号"] == 4]
    # luntai108_data = car1_data[car1_data["顺序编号"] == 5]
    # luntai109_data = car1_data[car1_data["顺序编号"] == 6]


    # print(len(excel1_g),len(data_g),len(car0_data),len(car1_data),len(luntai008_data))
    # 轮胎数据时间排序
    # # 牵引车时间排序
    luntai008_data = luntai008_data.sort_values(by="终端设备时间")
    luntai009_data = luntai009_data.sort_values(by="终端设备时间")
    luntai010_data = luntai010_data.sort_values(by="终端设备时间")
    luntai011_data = luntai011_data.sort_values(by="终端设备时间")
    # # 挂车时间排序
    # luntai100_data = luntai100_data.sort_values(by="终端设备时间")
    # luntai101_data = luntai101_data.sort_values(by="终端设备时间")
    # luntai102_data = luntai102_data.sort_values(by="终端设备时间")
    # luntai103_data = luntai103_data.sort_values(by="终端设备时间")
    # luntai108_data = luntai108_data.sort_values(by="终端设备时间")
    # luntai109_data = luntai109_data.sort_values(by="终端设备时间")
    # luntai110_data = luntai110_data.sort_values(by="终端设备时间")
    # luntai111_data = luntai111_data.sort_values(by="终端设备时间")

    # 毂温时间排序
    # luntai100_data = luntai100_data.sort_values(by="终端设备时间")
    # luntai101_data = luntai101_data.sort_values(by="终端设备时间")
    # luntai102_data = luntai102_data.sort_values(by="终端设备时间")
    # luntai103_data = luntai103_data.sort_values(by="终端设备时间")
    # luntai108_data = luntai108_data.sort_values(by="终端设备时间")
    # luntai109_data = luntai109_data.sort_values(by="终端设备时间")




    # 绘制时间轴图
    # # 牵引车时间
    dates8 = luntai008_data["终端设备时间"]
    dates9 = luntai009_data["终端设备时间"]
    dates10 = luntai010_data["终端设备时间"]
    dates11 = luntai011_data["终端设备时间"]
    # # 203 1
    # dates0 = luntai100_data["终端设备时间"]
    # dates1 = luntai101_data["终端设备时间"]
    # dates2 = luntai102_data["终端设备时间"]
    # dates3 = luntai103_data["终端设备时间"]
    # dates8 = luntai108_data["终端设备时间"]
    # dates9 = luntai109_data["终端设备时间"]
    # dates10 = luntai110_data["终端设备时间"]
    # dates11 = luntai111_data["终端设备时间"]
    # 毂温
    # dates0 = luntai100_data["终端设备时间"]
    # dates1 = luntai101_data["终端设备时间"]
    # dates2 = luntai102_data["终端设备时间"]
    # dates3 = luntai103_data["终端设备时间"]
    # dates8 = luntai108_data["终端设备时间"]
    # dates9 = luntai109_data["终端设备时间"]


    # # # 牵引车
    xs8 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S") for d in dates8]
    xs9 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S") for d in dates9]
    xs10 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S") for d in dates10]
    xs11 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S") for d in dates11]
    # # 挂车
    # xs0 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates0]
    # xs1 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates1]
    # xs2 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates2]
    # xs3 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates3]
    # xs8 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates8]
    # xs9 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates9]
    # xs10 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates10]
    # xs11 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates11]

    #  毂温
    # xs0 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates0]
    # xs1 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates1]
    # xs2 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates2]
    # xs3 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates3]
    # xs8 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates8]
    # xs9 = [datetime.strptime(d.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S") for d in dates9]




    fig = plt.figure(num=1)
    # ax = fig.add_subplot(1, 1, 1)
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))  # 设置时间标签显示格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M:%S'),)
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=8))

    # *******************for 胎压可视化*********************
    # ++++++++++++ 牵引车 ++++++++++++++
    plt.plot(xs8, luntai008_data["轮胎压力（Bar）"], 'rh:', markersize=3.5, label='0号轮胎胎压')
    plt.plot(xs9, luntai009_data["轮胎压力（Bar）"], 'gh:', markersize=3.5, label='1号轮胎胎压')
    plt.plot(xs10, luntai010_data["轮胎压力（Bar）"], 'ch:', markersize=3.5,  label='2号轮胎胎压')
    plt.plot(xs11, luntai011_data["轮胎压力（Bar）"], 'mh:', markersize=3.5, label='3号轮胎胎压')
    # ++++++++++++ 挂车 ++++++++++++++
    # plt.plot(xs0, luntai100_data["轮胎压力（Bar）"], 'rh:', markersize=3.5, label='0号轮胎胎压')
    # plt.plot(xs1, luntai101_data["轮胎压力（Bar）"], 'gh:', markersize=3.5, label='1号轮胎胎压')
    # plt.plot(xs2, luntai102_data["轮胎压力（Bar）"], 'ch:', markersize=3.5, label='2号轮胎胎压')
    # plt.plot(xs3, luntai103_data["轮胎压力（Bar）"], 'mh:', markersize=3.5, label='3号轮胎胎压')
    # plt.plot(xs8, luntai108_data["轮胎压力（Bar）"], color='#103005',linestyle=':',marker='h',markersize=3.5, label='8号轮胎胎压')
    # plt.plot(xs9, luntai109_data["轮胎压力（Bar）"], 'bh:', markersize=3.5, label='9号轮胎胎压')
    # plt.plot(xs10, luntai110_data["轮胎压力（Bar）"], 'yh:', markersize=3.5, label='10号轮胎胎压')
    # plt.plot(xs11, luntai111_data["轮胎压力（Bar）"], color='#FF6A6A', linestyle=':',marker='h',markersize=3.5, label='11号轮胎胎压')



    # *******************for 胎温可视化*********************
    # # ++++++++++++ 牵引车 ++++++++++++++
    # plt.plot(xs8, luntai008_data["轮胎温度（℃）"], 'rh:', markersize=3.5, label='0号轮胎胎温')
    # plt.plot(xs9, luntai009_data["轮胎温度（℃）"], 'gh:', markersize=3.5, label='1号轮胎胎温')
    # plt.plot(xs10, luntai010_data["轮胎温度（℃）"], 'ch:', markersize=3.5, label='2号轮胎胎温')
    # plt.plot(xs11, luntai011_data["轮胎温度（℃）"], 'mh:', markersize=3.5, label='3号轮胎胎温')
    # ++++++++++++ 挂车 ++++++++++++++
    # plt.plot(xs0, luntai100_data["轮胎温度（℃）"], 'rh:', markersize=3.5, label='0号轮胎胎温')
    # plt.plot(xs1, luntai101_data["轮胎温度（℃）"], 'gh:', markersize=3.5, label='1号轮胎胎温')
    # plt.plot(xs2, luntai102_data["轮胎温度（℃）"], 'ch:', markersize=3.5, label='2号轮胎胎温')
    # plt.plot(xs3, luntai103_data["轮胎温度（℃）"], 'mh:', markersize=3.5, label='3号轮胎胎温')
    # plt.plot(xs8, luntai108_data["轮胎温度（℃）"], color='#103005',linestyle=':',marker='h',markersize=3.5, label='8号轮胎胎温')
    # plt.plot(xs9, luntai109_data["轮胎温度（℃）"], 'bh:',markersize=3.5, label='9号轮胎胎温')
    # plt.plot(xs10, luntai110_data["轮胎温度（℃）"], 'yh:', markersize=3.5, label='10号轮胎胎温')
    # plt.plot(xs11, luntai111_data["轮胎温度（℃）"], color='#FF6A6A',linestyle=':',marker='h',markersize=3.5, label='11号轮胎胎温')


    #****************** 毂温可视化 *****************
    # plt.plot(xs0, luntai100_data["数据（℃）"], 'rh:',markersize=3.5, label='1号轮毂温度')
    # plt.plot(xs1, luntai101_data["数据（℃）"], 'gh:',markersize=3.5, label='2号轮毂温度')
    # plt.plot(xs2, luntai102_data["数据（℃）"], 'ch:',markersize=3.5, label='3号轮毂温度')
    # plt.plot(xs3, luntai103_data["数据（℃）"], 'mh:',markersize=3.5, label='4号轮毂温度')
    # plt.plot(xs8, luntai108_data["数据（℃）"], color='#103005', linestyle=':',marker='h',markersize=3.5, label='5号轮毂温度')
    # plt.plot(xs9, luntai109_data["数据（℃）"], 'bh:',markersize=3.5, label='6号轮毂温度')





    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.title("208车牵引车轮压力度时序监测")
    plt.xlabel('时间')
    plt.ylabel('轮胎压力（Bar）')
    # plt.ylabel('轮胎温度（℃）')
    # plt.ylabel('轮毂温度（℃）')
    plt.legend()
    plt.grid(True,linestyle=':', linewidth=0.5)
    plt.show()














    # print(luntai008_data)
    # print(luntai08_data[["轮胎温度（℃）", "轮胎压力（Bar）"]].describe())
    # print(luntai08_data.dtypes)
    # print('----------------分割线-------------------')
    # tim = luntai08_data["终端设备时间"]
    # tim_one = tim[110636]
    # print(tim_one,type(tim_one))

    # print(tim,type(tim))
    # print(tim_one,type(tim_one))
    # print(xs,len(xs))
    # print(dt,type(dt))
    # print(dt + timedelta(hours=8))


if __name__ == '__main__':
    # read_excel()
    # read_excel_wtpd()
    # test()
    # read_excel_threshold()
    # read_excel_threshold_compare()
    read_excel_time_axis()

