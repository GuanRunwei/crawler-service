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


def get_yidong(request):
    YiDong_dict = {
        8202: "快速反弹",
        8201: "火箭发射",
        64: "有大买盘",
        8210: "低开5日线",
        8203: "高台跳水",
        8193: "大笔买入",
        8194: "大笔卖出",
        128: "有大卖盘",
        8204: "加速下跌",
        8208: "竞价下跌",
        8213: "60日新高",
        8216: "60日大幅下跌",
        4: "封涨停板",
        8215: "60日大幅上涨",
        16: "打开涨停板",
        8: "封跌停板",
        32: "打开涨跌板",
        8209: "高开5日线",
        8214: "60日新低",
        8207: "竞价上涨",
        8212: "向下缺口",
        8211: "向上缺口",
    }
    page_index, final_result = int(request.GET["PageNumber"]) - 1, []
    try:
        url = "http://push2ex.eastmoney.com/getAllBKChanges?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzchanges&pageindex=0&pagesize=50" + "&pageindex=" + str(
            page_index)
        response = SendRequest(url=url, header=headers)
        data = json.loads(response.get_initial_data())
        if data["data"] is None:
            return JsonResponse({"code": 400, "data": "暂无当日异动数据"}, safe=False)
        for i in range(len(data["data"]["allbk"])):
            final_result.append(
                {
                    "板块名称": data["data"]["allbk"][i]["n"],
                    "涨跌幅": data["data"]["allbk"][i]["u"] + "%",
                    "主力净流入": Number_util.num_check(data["data"]["allbk"][i]["zjl"]),
                    "板块异动总次数": data["data"]["allbk"][i]["ct"],
                    "板块异动最频繁个股及所属类型": data["data"]["allbk"][i]["ms"]["n"] + "(" + YiDong_dict[data["data"]["allbk"][i]["ms"]["t"]] + ")",
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][0]["t"]]: data["data"]["allbk"][i]["ydl"][0]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][1]["t"]]: data["data"]["allbk"][i]["ydl"][1]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][2]["t"]]: data["data"]["allbk"][i]["ydl"][2]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][3]["t"]]: data["data"]["allbk"][i]["ydl"][3]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][4]["t"]]: data["data"]["allbk"][i]["ydl"][4]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][5]["t"]]: data["data"]["allbk"][i]["ydl"][5]["ct"],
                    YiDong_dict[data["data"]["allbk"][i]["ydl"][6]["t"]]: data["data"]["allbk"][i]["ydl"][6]["ct"],
                }
            )
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse({"code": 200, "page": 7, "data": final_result}, safe=False)











