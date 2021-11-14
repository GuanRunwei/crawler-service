import json
from util.SendRequest import SendRequest
from util.number_util import Number_util
from django.http import JsonResponse

headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': '42.push2.eastmoney.com',
               'Referer': "http://quote.eastmoney.com/center/gridlist.html",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
           }


def get_worldstock_index(request):
    url = "http://42.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=i:1.000001,i:0.399001,i:0.399005,i:0.399006,i:1.000300,i:100.HSI,i:100.HSCEI,i:124.HSCCI,i:100.TWII,i:100.N225,i:100.KOSPI200,i:100.KS11,i:100.STI,i:100.SENSEX,i:100.KLSE,i:100.SET,i:100.PSI,i:100.KSE100,i:100.VNINDEX,i:100.JKSE,i:100.CSEALL&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107&_=1584063319092"
    final_result = []
    try:
        response = SendRequest(url=url, header=headers)
        initial_data = json.loads(response.get_initial_data())
        data = initial_data["data"]["diff"]
        for item in data:
            final_result.append({"股指名": item["f14"], "最新价": str(item["f2"]), "涨跌额": str(item["f4"]), "涨跌幅": str(item["f3"]) + "%"})

    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse({"code": 200, "data": final_result}, safe=False)

