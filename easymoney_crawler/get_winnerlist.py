import json
import math
import datetime
from util.SendRequest import SendRequest
from util.number_util import Number_util
from django.http import JsonResponse
import logging
import time
from multiprocessing.dummy import Pool as ThreadPool


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "data.eastmoney.com",
    "Referer": "http://data.eastmoney.com/stock/tradedetail.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
}

final_result = []


# def get_logger(name):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.DEBUG)
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(logging.DEBUG)
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
#     stream_handler.setFormatter(formatter)
#     logger.addHandler(stream_handler)
#     return logger
#
#
# def process(item):
#     log = get_logger(item["SName"])
#     log.info("item: %s" % item)
#     time.sleep(0.0001)
#     final_result.append(
#         {"代码": item["SCode"], "名称": item["SName"], "上榜日": item["Tdate"], "上榜原因": item["Ctypedes"],
#          "解读": item["JD"], "收盘价": item["ClosePrice"], "涨跌幅": item["Chgradio"],
#          "龙虎榜净买额": Number_util.convert_stringnumber(item["JmMoney"]), "龙虎榜买入额": Number_util.convert_stringnumber(item["Bmoney"]),
#          "龙虎榜成交额": Number_util.convert_stringnumber(item["ZeMoney"]), "市场总成交额": Number_util.convert_stringnumber(item["Turnover"]),
#          "净买额占总成交比": item["JmRate"] + "%", "成交额占总成交比": item["ZeRate"] + "%", "换手率": item["Dchratio"] + "%",
#          "流通市值": Number_util.convert_stringnumber(item["Ltsz"])
#          })


def get_winnerlist(request):
    start_date, end_date = request.GET["StartDate"], request.GET["EndDate"]
    page = request.GET["Page"]
    try:
        url = "http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=" + start_date + ",endDate=" + end_date + ",gpfw=0,js=.html?rt=26398232"
        response = SendRequest(url=url, header=headers)
        initial_data = json.loads(response.get_initial_data())
        if len(initial_data["data"]) >= 20 * int(page):
            stock_list = initial_data["data"][20*(int(page)-1):20*int(page)]
        else:
            if 20 * (int(page)-1) < len(initial_data["data"]) < 20 * int(page):
                stock_list = initial_data["data"][20*(int(page)-1):len(initial_data["data"])]
            else:
                return JsonResponse({"code": 400, "data": "没有更多数据了"},
                                    safe=False)
        for item in stock_list:
            final_result.append(
                {"代码": item["SCode"], "名称": item["SName"], "上榜日": item["Tdate"], "上榜原因": item["Ctypedes"],
                 "解读": item["JD"], "收盘价": item["ClosePrice"], "涨跌幅": item["Chgradio"],
                 "龙虎榜净买额": Number_util.convert_stringnumber(item["JmMoney"]), "龙虎榜买入额": Number_util.convert_stringnumber(item["Bmoney"]),
                 "龙虎榜成交额": Number_util.convert_stringnumber(item["ZeMoney"]), "市场总成交额": Number_util.convert_stringnumber(item["Turnover"]),
                 "净买额占总成交比": item["JmRate"] + "%", "成交额占总成交比": item["ZeRate"] + "%", "换手率": item["Dchratio"] + "%",
                 "流通市值": Number_util.convert_stringnumber(item["Ltsz"])
                 })
    except Exception:
        print(Exception.__str__())
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)
    return JsonResponse({"code": 200, "上榜股票数": len(initial_data["data"]), "page": page, "data": final_result}, safe=False)
