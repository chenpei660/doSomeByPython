import traceback

import numpy as np

import json
import urllib.request
import urllib
import os
import time
#连接数据库


now = int(time.time())
#转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
timeStruct = time.localtime(now)
strTime = time.strftime("%Y-%m-%d", timeStruct)
gp_count = 1        #股票当天所有数据的保存编号
print("start")
def mkdir(path):    #股票保存路径函数
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print(path)
def getData(url):   #函数——从接口中获取单只股票当天每分钟的数据
    #content = ""
    try:        #网络会偶发出现奔溃情况，为了保证不中断和保证数据齐全，休息5秒重新执行
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
                   "Cookie":"ga=GA1.2.1883806091.1541942213; device_id=24700f9f1986800ab4fcc880530dd0ed; s=bz12e2nrf9; cookiesu=541581901909562; xq_a_token=9950c70144836700003fcfca7863f339a5cea71d; xqat=9950c70144836700003fcfca7863f339a5cea71d; xq_r_token=30a00404c7d032b2aa77b5d637d348f65c16771b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjk1MDY5NTQwMjMsImlzcyI6InVjIiwiZXhwIjoxNTg0NDk4NDAxLCJjdG0iOjE1ODE5MDY0MDEzNDgsImNpZCI6ImQ5ZDBuNEFadXAifQ.c6WxgkS1C-2qgRgy9l2c0qKd_UlexD1InrApC2KSntnnkk5lFU93H5zxk5DfyqwjowIa6LdpcxWaPOx25sUxsoAJhEEy8QnJhCve_YoxmqwQUPNJzHKx5KgS3Kop6TduwJhkU9KvDOTIwhPGjXg7TuBm9x23yHnlfuaPkjkeXLsUCaaB4Dc3LPi-Pjq6VAk1y1KoAQW5Unw41FGm9_Pcf0MRlnKGVIE7LYrHC6lLNgUPFQunZ9-fQ3ZMS_9lFVKPyfqeWv4tyzybFZo-P2K8XPB6Cb7vtZ04sp-_nP6cf0TMTClFBQaB-ffCXJHuh9zqjRqeK_d9zbbhl3WV-iF1AA; xq_token_expire=Fri%20Mar%2013%202020%2010%3A26%3A41%20GMT%2B0800%20(China%20Standard%20Time); xq_is_login=1; u=9506954023; bid=5da0e31c8428139e81ddb8517deffb31_k6pu87gc; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1581471756,1581900937,1581908266,1582075640; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1582186956"}
        req =urllib.request.Request(url, None, headers)
        header=urllib.request.HTTPHandler()
        opener=urllib.request.build_opener(header)
        response=opener.open(req)
        print(response)
        print("dd")

        content = response.read()

    except BaseException as cc:
        print("发生网络异常")
        print(traceback.print_exc())
        #print(str(cc))
        time.sleep(5)
        return ""
    if content != "":
        return content
    else:
        print("内容为空")
        return getData(url)
def csv_create(path, msg):     #函数——将单只股票的数据保存进指定文件夹
    file = open(path,'w')
    file.write(msg)
    print("文件"+path+"创建成功")
    file.close()
def tranformToCSV(content,filepath,fileName):        #函数——将下载的数据转换为csv数据，以便读取
    json_str = content
    symbol = json_str.get("symbol")
    column = json_str.get("column")
    itemss = json_str.get("item")
    mkdir(filepath)
    array_str = np.array(itemss)
    csv_str = ''
    # 组装表头
    for col in column:
        csv_str +=str(col)+"," # "time,first,second,third,fourth\n"    #time为当天时间点，first为该分钟股票价格
        if col == 'timestamp':
            csv_str += 'day,'  # 添加 年月日的列
    csv_str +="\n"
    for itemList in array_str:
        #item = str(item)

        for columnItem in itemList:
            csv_str += str(columnItem)+','
            if columnItem == itemList[0]: #  额外将时间戳变为年月日，并添加在新增列 day 中
                print(int(columnItem)/1000)
                print(time.localtime(int(columnItem)/1000))
                csv_str += time.strftime("%Y-%m-%d",time.localtime(int(columnItem)/1000))+','

        csv_str += '\n'
        #csv_str += '",'+str(item[1])+','+str(item[2])+','+str(item[3])+','+str(item[4])+'\n'
    print(symbol)
    csv_create(filepath+fileName,csv_str)

def downloadStock(stockCode,type): # 下载指定股票的三种复权价格
    #url = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&id="+item[3]+item[1]+"&type=r&iscr=false"
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol="+stockCode+"&begin=1582273377552&period=day&type="+type+"&count=-2000&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance";
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol="+stockCode+"&begin=1582273377552&period=day&type="+type+"&count=-2000&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance";
    data = getData(url)
    print(data)
    print("end")
    res = json.loads(data)
    print(res.get("data"))
    print(res.get("error_code"))
    #item2 = item[2].replace("*","")
    tranformToCSV(res.get("data"),"D://gp/"+stockCode+'/',stockCode+'-'+type+'.csv')     #股票信息的保存路径是（D：//pg/序号+股票名字+股票代号/日期.csv）

def downloadAllType(stockCode):
    downloadStock(stockCode,"before")
    downloadStock(stockCode,"normal")
    downloadStock(stockCode,"after")

# 主模块
if __name__ == "__main__":
    downloadAllType('SH601939')




