# -*- coding: utf8 -*-
import urllib
import urllib2
import random
import re
import time
import cookielib


def requestUrl(url, form=None):
    #Get
    if None == form:
        req = urllib2.Request(url)
    #Post
    else:
        headers = {
            #模拟的是IE
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/",
            'X-Requested-With': "XMLHttpRequest"
        }
        req = urllib2.Request(url, urllib.urlencode(form), headers)
    
    response = urllib2.urlopen(req)
    #TODO:处理返回错误
    data = response.read()
    return data


def saveDataToFile(strData, path, fileName):
    f = open(path+'/'+fileName, "wb")
    f.write(strData)
    f.close()

def requestGet(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    global g_cookie
    g_cookie.save()
    return data


def getCaptcha():
    captcha_url = 'http://www.zhihu.com/captcha.gif?r='+str(long(time.time()*1000))
    data = requestUrl(captcha_url)
    f = open("captcha.gif", "wb")
    f.write(data)
    f.close()
    captcha = raw_input("captcha:")
    return captcha

def getXsrf():
    url = "http://www.zhihu.com/#signin"
    #url = "http://www.zhihu.com/"
    data = requestUrl(url)
    pattern_xsrf = re.compile(r'name="_xsrf" value="([^"]*)"')
    result = pattern_xsrf.findall(data)
    return result[0]


def setSession():
    #url = "http://www.zhihu.com/settings/profile"
    url = "http://www.zhihu.com/settings/account"

    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)


def login(account, password, remember_me):
    setSession()
    form = {}
    #account
    form["email"] = account
    #password
    form["password"] = password
    # _xsrf
    form["_xsrf"] = getXsrf()
    #remember_me
    form["remember_me"] = remember_me
    #captcha
    form["captcha"] = getCaptcha()
    
    login_url = "http://www.zhihu.com/login/email"
    data = requestUrl(login_url, form)
    print(data)


if "__main__" == __name__:
    login("email@qq.com", "password", "true")
    #login()
