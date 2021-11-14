import json
import math
import datetime
from util.SendRequest import SendRequest
from util.number_util import Number_util
from django.http import JsonResponse


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': '74.push2.eastmoney.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
           }

All_Field = \
    {
        "nowPrice": "f2",
        "diff_rate": "f3",
        "diff_money": "f4",
        "tradeAmount": "f5",
        "turnover": "f8",
        "pe": "f9",
        "pb": "f23"

    }


def is_number(item):
    if type(item["f2"]) is not str and \
            type(item["f3"]) is not str and type(item["f4"]) is not str \
            and type(item["f5"]) is not str and type(item["f8"]) is not str \
            and type(item["f9"]) is not str and type(item["f23"]) is not str:
        return True
    return False


def get_kechuang(request):
    page = request.GET["Page"]
    sort_field = request.GET["SortField"]
    sort_type = request.GET["SortType"]
    url = "http://13.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:23&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62&_=1585819086668"
    initial_data = json.loads(SendRequest(url, header=headers).get_initial_data())
    final_result = []
    try:
        if sort_type is "1":
            initial_data = sorted(filter(is_number, initial_data["data"]["diff"]),
                                  key=lambda x: x[All_Field[sort_field]], reverse=False)
        else:
            initial_data = sorted(filter(is_number, initial_data["data"]["diff"]),
                                  key=lambda x: x[All_Field[sort_field]], reverse=True)
        if 20 * int(page) <= len(initial_data):
            stock_list = initial_data[(int(page) - 1) * 20:int(page) * 20]
        else:
            if 20 * (int(page) - 1) < len(initial_data) < 20 * int(page):
                stock_list = initial_data[20 * (int(page) - 1):len(initial_data)]
            else:
                return JsonResponse({"code": 400, "data": "没有更多数据了"},safe=False)
        for item in stock_list:
            final_result.append(
                {"code": item["f12"], "name": item["f14"], "nowPrice": item["f2"], "diff_rate": str(item["f3"]) + "%",
                 "diff_money": item["f4"], "tradeAmount": Number_util.num_check(item["f5"]),
                 "turnover": str(item["f8"]) + "%", "pe": str(item["f9"]) + "%", "pb": str(item["f23"]) + "%"})
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)
    return JsonResponse({"code": 200, "上榜股票数": len(initial_data), "page": page, "data": final_result}, safe=False)



