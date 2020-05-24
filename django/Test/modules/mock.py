from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import traceback
import random
import json
import re
import hashlib
import os

print(os.path.abspath('.')) #获得的是当前执行脚本的位置

@csrf_exempt
def activityConfig(request):
    request.body
    if re.search(r'/H5/Outdoorsrank/getDayRank',request.path,re.M|re.I):
        imgUrl = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2884589004,2156092328&fm=27&gp=0.jpg'
        data = {
            'error': 0,
            'data': {
                'list':[

                ],
                'rankInfo': { #主播排名信息
                    'sc': 32000000,  #积分 （直接透传c++数据未处理）
                    'rank': 1		#排名
                }   
            }
        }
        i = 1
        while i <= random.randint(1,10):
            data['data']['list'].append(
                {
                    'idx': i,  #排名
                    'room_id': 273878,#房间id
                    'nickname': "我是谁", #主播名
                    'avatar': imgUrl,#主播头像
                    'is_vertical': False, #是否竖屏 true 是 false是
                    'vertical_src': "https:#fangjie_dy.dz11.com/upload/web_pic/amrpic-180505/273878_1020_thumb.jpg", #封面
                    'sc': random.randint(1,99999) #积分 （直接透传c++数据未处理）
                }
            )
            i += 1
    elif re.search(r'/H5/Outdoorsrank/getAllRank',request.path,re.M|re.I):
        imgUrl = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2884589004,2156092328&fm=27&gp=0.jpg'
        data = {
            'error': 0,
            'data': {
                'list':[{
                        'idx': 1,  #排名
                        'room_id': 273878,#房间id
                        'nickname': "test201660000052", #主播名
                        'avatar': imgUrl,#主播头像
                        'is_vertical': False, #是否竖屏 true 是 false是
                        'vertical_src': "https:#fangjie_dy.dz11.com/upload/web_pic/amrpic-180505/273878_1020_thumb.jpg", #封面
                        'sc': random.randint(1,99999) #积分 （直接透传c++数据未处理）
                    },
                ],
                'rankInfo': { #主播排名信息
                    'sc': 32000000,  #积分 （直接透传c++数据未处理）
                    'rank': 1		#排名
                }   
            }
        }
    elif re.search(r'/H5/Outdoorsrank/getCycleList',request.path,re.M|re.I):
        data = {
            'code': 0,
            'data': {
                1: {
                    'date': 1526054400,
                    'cur': 0
                },
                2: {
                    'date': 1526140800,
                    'cur': 0
                },
                3: {
                    'date': 1526227200,
                    'cur': 0
                },
                4: {
                    'date': 1526313600,
                    'cur': 0
                },
                5: {
                    'date': 1526400000,
                    'cur': 1
                },
                6: {
                    'date': 1526486400,
                    'cur': 0
                }
            }
        }
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = request.META['HTTP_ORIGIN']   #设置允许源
    return response