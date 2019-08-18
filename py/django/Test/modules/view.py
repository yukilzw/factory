from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .. import models
import configparser
import traceback
import urllib
import re
import uuid
import json
import time
import hashlib
import threading
import os
import copy
from . import wxToken
#from . import opencv

#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/url.conf'
    config.read(path)
    return config.get(section, key)

PUBLIC = {
    "req_url" : getConfig("url","req_url")
}

#获取微信assess_token,jsapi_ticket
if PUBLIC["req_url"] == "http://liuzhanwei.tunnel.echomod.cn/":
    wxCheck = wxToken.getAssessToken()

#404返回
is404 = lambda req: HttpResponse(404)

#请求转发
@csrf_exempt
def pipe(request):
    if re.search(r'pipe',request.path,re.M|re.I):
        url = "http://localhost:1234" + request.path
    reqHeaders = {}    #转发请求头
    for k,val in request.META.items():
        if re.search(r'^content', k, re.M|re.I) or re.search(r'^http', k, re.M|re.I):
            reqHeaders[ re.sub(r'http_', "", k , flags = re.M|re.I).lower() ] = val
    data = urllib.parse.urlencode(request.POST).encode("utf-8") #转发数据
    req = urllib.request.Request(url, data, reqHeaders) #http请求
    res = urllib.request.urlopen(req)   #http返回
    the_page = res.read()   #返回数据解析
    print(the_page.decode("utf-8"))
    response = HttpResponse(the_page)
    for val in res.headers._headers:  #过滤不被允许的 hop-by-hop headers
        if ( val[0] != "Connection" ) and ( val[0] != "Transfer-Encoding" )\
        and ( val[0] != "Keep-Alive" ) and ( val[0] != "Server" ):
            response[ val[0] ] = val[1]
    response["Access-Control-Allow-Origin"] = request.META['HTTP_ORIGIN']   #设置允许源
    return response

#主页
def home(request):
    '''
    sqlDate = {
        "id":uuid.uuid1().hex,
        "name": "刘占威",
        "tel": 13871519390
    }
    obj = models.Company.objects.create(**sqlDate)
    '''
    data = {
        "title":"个人主页|刘占威",
        "content":"心动音符丶",
    }
    return render(request, 'home.html',data)

#vue spa demo
def vueDemo(request):
    files = os.path.join("../../js-frame/by-vue/client-dist/index.html")
    with open(files,mode='r', encoding='UTF-8') as f:
        response = HttpResponse(f.read())
    return response   
    
#微信测试号验证
def wxToken(request):
    response = HttpResponse(request.GET['echostr'])
    return response

#微信网页接口JS-SDK验证
def wx_JSSDK_check(request):
    url = request.GET['url']
    nonceStr = uuid.uuid1().hex
    timestamp = str(int(time.time()))
    _str = 'jsapi_ticket='+wxCheck.ticket+ \
           '&noncestr='+nonceStr+ \
           '&timestamp='+timestamp+ \
           '&url='+url
    signature = hashlib.sha1(_str.encode("utf-8")).hexdigest()
    res_dic = {
        "appId":"wx73648417a7f020b2",
        "nonceStr":nonceStr,
        "timestamp":timestamp,
        "signature":signature
    }
    response = JsonResponse(res_dic)
    return response

#获取微信openId,昵称,头像
def wxOpenId(request):
    url = request.GET['url']
    code = request.GET['code']
    if url:
        data = {
            "appid":"wx73648417a7f020b2",
            "redirect_uri":url,
            "response_type":"code",
            "scope":"snsapi_userinfo",
        }
        urlencode = urllib.parse.urlencode(data)
        res_dic = {
            "status":True,
            "codeUrl":"https://open.weixin.qq.com/connect/oauth2/authorize?"+urlencode+"#wechat_redirect",
        }
    elif code:
        res_dic = {
            "status":True
        }
        data = {
            "appid":"wx73648417a7f020b2",
            "secret":"99c1a2788f166198b991c688bc19bd8c",
            "code":code,
            "grant_type":"authorization_code",
        }
        urlencode = urllib.parse.urlencode(data)
        req = urllib.request.Request("https://api.weixin.qq.com/sns/oauth2/access_token?"+urlencode)
        res = urllib.request.urlopen(req)
        res_data =  json.loads( res.read() )
        res_dic["openid"] = res_data["openid"]
        data = {
            "access_token": res_data["access_token"],
            "openid": res_data["openid"],
            "lang": "zh_CN",
        }
        urlencode = urllib.parse.urlencode(data)
        req = urllib.request.Request("https://api.weixin.qq.com/sns/userinfo?"+urlencode)
        res = urllib.request.urlopen(req)
        res_data =  json.loads( res.read() )
        res_dic["nickname"] = res_data["nickname"]
        res_dic["photoUrl"] = res_data["headimgurl"]
    response = JsonResponse(res_dic)
    response["Access-Control-Allow-Origin"] = request.META['HTTP_HOST']
    return response

#微信推送人脸识别消息
@csrf_exempt
def wxMsgPush(request):
    dic = {
        "touser":request.POST["openId"],
        "template_id":"lkhk2WF1npyi9_TOmFfqS--2J4CbSaY6lAsc8yHGOO0",
        "topcolor":"#FF0000",
        "data":{
            "sex":{
                "value":request.POST["sex"],
                "color":"#333333"
            },
            "age":{
                "value":request.POST["age"],
                "color":"#333333"
            },
            "race":{
                "value":request.POST["race"],
                "color":"#333333"
            },
            "emotion":{
                "value":request.POST["emotion"],
                "color":"#333333"
            },
            "stain":{
                "value":request.POST["stain"],
                "color":"#333333"
            },
            "acne":{
                "value":request.POST["acne"],
                "color":"#333333"
            },
            "dark_circle":{
                "value":request.POST["dark_circle"],
                "color":"#333333"
            },
            "health":{
                "value":request.POST["health"],
                "color":"#333333"
            },
            "grade":{
                "value":request.POST["grade"],
                "color":"#5400FF"
            },
        }
    }
    data = re.sub(r'\'', "\"",str(dic)).encode("utf-8")
    req = urllib.request.Request("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="+wxCheck.assess_token,data)
    res = urllib.request.urlopen(req)
    res_data = json.loads(res.read())
    response = JsonResponse(res_data)
    response["Access-Control-Allow-Origin"] = request.META['HTTP_HOST']
    return response

#opencv人脸识别
@csrf_exempt
def savePhotoImg(request):
    stat = {'status':False,'path':None,'msg':None}
    if request.method != "POST":
        response = JsonResponse(stat)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    try:
        img = request.FILES['the_file']
        t = str( time.time() )
        img_path = os.path.join('./Test/static/face/newface/',t)
        with open(img_path,'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        cv2 = opencv.findFace(img.name,t)
        stat['status'] = True
        stat['path'] = cv2.path
        stat['res_path'] = cv2.res_path
        stat['msg'] = '识别成功'
        if not len(cv2.res_path):
            stat['status'] = False
            stat['msg'] = '算法不给力,识别不了这张图\n\n/(ㄒoㄒ)/~~'
    except Exception as e:
        stat['msg'] = str(e)
        print('savePhotoImg Error：'+str(e))
    finally:
        response = JsonResponse(stat)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#face++人脸识别
@csrf_exempt
def binaryPipe(request):
    request.body
    def save(fileName,picName):
        img = request.FILES[fileName]
        md5 = hashlib.md5()
        md5.update( (request.POST[picName] + str(img.size)).encode() )
        name = md5.hexdigest() + "." + request.POST[picName].split(".")[-1]
        img_path = os.path.join('./Test/static/face/newface/',name)
        if not os.path.exists(img_path):
            with open(img_path,'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
        stat['path'].append('py/static/face/newface/' + name)
    def recognition(name):
        data = {
            "api_key":"Myzf_TjfV1z0Wm3ld2sraH6VRpXMlTGJ",
            "api_secret" : "cWkQGRkTed14h8kWOrxA80cBEsFvY4Cv",
            "image_url":PUBLIC["req_url"]+"py/static/face/newface/"+name,
            "return_attributes": "gender,age,headpose,smiling,eyestatus,mouthstatus,beauty,facequality,skinstatus,ethnicity,emotion"
        }
        if len(json.loads(request.POST["path"])) == 1:
            data["return_landmark"] = 1
        data = urllib.parse.urlencode(data).encode("utf-8")
        #headers = {'user_agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
        req = urllib.request.Request("https://api-cn.faceplusplus.com/facepp/v3/detect", data)
        try:
            res = urllib.request.urlopen(req)
            the_res = res.read()
            stat['result'].append(json.loads(the_res))
        except urllib.error.HTTPError as e:
            error = json.loads(e.read())
            if error["error_message"] == "CONCURRENCY_LIMIT_EXCEEDED":
                print("CONCURRENCY_LIMIT_EXCEEDED")
                recognition(name)
            else:     
                raise Exception(e)
    def compare(path):
        isSameFace = [True]
        def compareTwoPic(img1,img2):
            if not isSameFace[0]:
                return
            data = {
                "api_key":"Myzf_TjfV1z0Wm3ld2sraH6VRpXMlTGJ",
                "api_secret" : "cWkQGRkTed14h8kWOrxA80cBEsFvY4Cv",
                "image_url1":PUBLIC["req_url"]+img1,
                "image_url2":PUBLIC["req_url"]+img2,
            }
            data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request("https://api-cn.faceplusplus.com/facepp/v3/compare", data)
            try:
                res = urllib.request.urlopen(req)
                result = json.loads( res.read() )
                if result["confidence"] < result["thresholds"]["1e-3"]:
                    isSameFace[0] = False
            except urllib.error.HTTPError as e:
                error = json.loads(e.read())
                if error["error_message"] == "CONCURRENCY_LIMIT_EXCEEDED":
                    print("CONCURRENCY_LIMIT_EXCEEDED")
                    compareTwoPic(img1,img2)
                else:     
                    raise Exception(e)
        compareTwoPic(path[0],path[1])
        compareTwoPic(path[1],path[2])
        del stat["path"],stat["msg"]
        stat["result"] = isSameFace[0]
    stat = {'status':False,'path':[],'result':[],'msg':None}
    try:
        length,i= 0,0
        if request.POST["reqType"] == "save":
            length = len(request.FILES.keys())
        elif request.POST["reqType"] == "recognition":
            length = len(json.loads(request.POST["path"]))
        elif request.POST["reqType"] == "compare":
            compare( json.loads(request.POST["path"]) )
        while i < length:
            _i = str(i)
            if request.POST["reqType"] == "save":
                save("image_file"+_i,"name"+_i)
                stat['msg'] = '上传成功'
            elif request.POST["reqType"] == "recognition":
                recognition( json.loads(request.POST["path"])[i].split("/")[-1] )
                stat['msg'] = '识别成功'
            i+=1
        stat['status'] = True
    except Exception as e:
        stat['path'],stat['result'] = [],[]
        stat['msg'] = "接口调用失败，请重试"
        print( traceback.print_exc() )
    finally:
        response = JsonResponse(stat)
        response["Access-Control-Allow-Origin"] = "*"
        return response