import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import random
import time
import lxml


# class IDCard():
def regiun(strarr):
    '''生成身份证前六位'''
    first = random.choice(strarr)
    return first


def year():
    '''生成年份'''
    # 1978为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
    now = time.strftime('%Y')
    second = random.randint(1978, int(now) - 18)
    # age = int(now)-second
    # print('随机生成的身份证人员年龄为：'+str(age))
    return second


def month():
    '''生成月份'''
    three = random.randint(1, 12)
    if three < 10:
        three = '0' + str(three)
        return three
    else:
        return three


def day(year, month):
    '''生成日期'''
    four = getDay(year, month)
    # 日期小于10以下，前面加上0填充
    if four < 10:
        four = '0' + str(four)
        return four
    return four


def getDay(year, month):
    '''根据传来的年月份返回日期'''
    # 1，3，5，7，8，10，12月为31天，4，6，9，11为30天，2月闰年为28天，其余为29天
    aday = 0
    if month in (1, 3, 5, 7, 8, 10, 12):
        aday = random.randint(1, 31)
    elif month in (4, 6, 9, 11):
        aday = random.randint(1, 30)
    else:
        # 即为2月判断是否为闰年
        if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            aday = random.randint(1, 28)
        else:
            aday = random.randint(1, 29)
    return aday


def randoms():
    '''生成身份证后四位'''
    five = random.randint(1, 9999)
    if five < 10:
        five = '000' + str(five)
    elif 10 < five < 100:
        five = '00' + str(five)
    elif 100 < five < 1000:
        five = '0' + str(five)
    return five



def idcard(fpath):
    # 通过爬取网页获取到身份证前六位
    with open(fpath,'r') as f:
        strarr = []
        for line in f:
            strarr.append(line.split()[0])
    for i in range(1, 2):
        first = regiun(strarr)
        second = year()
        three = month()
        four = day(second, three)
        last = randoms()
        IDCard = str(first) + str(second) + str(three) + str(four) + str(last)
        # print('随机生成的身份证号码为：' + IDCard)
    return IDCard

if __name__ == '__main__':
    limit = 800
    for i in range (800):
        print (idcard('./ID_generate/strarr'))