# -*- coding: utf8 -*-
import random
import re
import time
import requests

#session请求
sessionRequests = requests.Session()


'''
@beif
@params data 要传的参数
'''
def requestUrl(url, data=None):
    global sessionRequests
    #Get
    if None == data:
        response = sessionRequests.get(url)
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
        response = sessionRequests.post(url, data=data, headers=headers)
    #print response.status_code
    #print response.headers
    #print response.cookies

    return response.content

'''
    保存数据到文件里面
'''
def saveDataToFile(strData, path, fileName):
    
    f = open(path+'/'+fileName, "wb")
    f.write(strData)
    f.close()

'''
@brief 获取验证码,保存到当前文件夹里面
'''
def getCaptcha():
    captcha_url = 'http://www.zhihu.com/captcha.gif?r='+str(long(time.time()*1000))
    data = requestUrl(captcha_url)
    f = open("captcha.gif", "wb")
    f.write(data)
    f.close()
    captcha = raw_input("captcha:")
    return captcha

'''
@brief 获取_xsrf
'''
def getXsrf():
    url = "http://www.zhihu.com/#signin"
    #url = "http://www.zhihu.com/"
    data = requestUrl(url)
    pattern_xsrf = re.compile(r'name="_xsrf" value="([^"]*)"')
    result = pattern_xsrf.findall(data)
    return result[0]

'''
'''
def setSession():
    #url = "http://www.zhihu.com/settings/profile"
    url = "http://www.zhihu.com/settings/account"
    requestUrl(url)

'''
@brief 获取某个问题
@params questionNumber 问题的编号
'''
def getQuestionMsg(questionNumber):
    print("get question msg...")
    question_url = "http://www.zhihu.com/question/"+str(questionNumber)
    data = requestUrl(question_url)
    saveDataToFile(data, ".", "question"+str(questionNumber)+'.html')

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
    #getQuestionMsg(34580301)
    #login()

