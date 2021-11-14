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


def get_single_plate(request):
    try:
        url = "http://74.push2.eastmoney.com/api/qt/clist/get?po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&_=1582597649159&pn=1"
        request = SendRequest(url, headers)
        s_initial = request.get_initial_data()
        s = json.loads(s_initial)
        return JsonResponse({"plate": str(s["data"]["diff"][0]["f14"])}, safe=False)
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)


def get_rate_rank_top5():
    url = "http://74.push2.eastmoney.com/api/qt/clist/get?po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&_=1582597649159&pn=1"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    data_num = len(s["data"]["diff"])
    final_result = {}
    final_list = []
    if data_num >= 5:
        for i in range(5):
            temp_dict = {str(s["data"]["diff"][i]["f14"]): str(s["data"]["diff"][i]["f3"])+"%"}
            final_list.append(temp_dict)
    else:
        for i in range(5):
            temp_dict = {s["data"]["diff"][i]["f14"]: str(s["data"]["diff"][i]["f3"]) + "%"}
            final_list.append(temp_dict)
    final_result["今日涨幅最大"] = final_list
    return final_result


def get_rate_rank_industry():
    final_result = {}
    final_list = []
    for j in range(4):
        url = "http://89.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222" + "&pn=" + str(j+1)
        request = SendRequest(url, headers)
        s_initial = request.get_initial_data()
        s = json.loads(s_initial)
        data_num = len(s["data"]["diff"])

        for i in range(data_num):
            temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                         "涨跌额": str(s["data"]["diff"][i]["f14"]),
                         "总市值": Number_util.num_check(s["data"]["diff"][i]["f20"]),
                         "换手率": str(s["data"]["diff"][i]["f8"]) + "%", "上涨家数": str(s["data"]["diff"][i]["f104"]),
                         "下跌家数": str(str(s["data"]["diff"][i]["f105"])),
                         "最新价": str(s["data"]["diff"][i]["f2"]), "领涨股": str(s["data"]["diff"][i]["f128"]),
                         "代码": str(s["data"]["diff"][i]["f140"]), "领涨股涨幅": str(s["data"]["diff"][i]["f136"])}
            final_list.append(temp_dict)
    final_result["行业板块"] = final_list
    return final_result


def get_rate_rank_industry_top6():
    final_result = {}
    final_list = []
    url = "http://89.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&pn=1"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    for i in range(6):
        temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                     "领涨股": str(s["data"]["diff"][i]["f128"])}
        final_list.append(temp_dict)
    final_result["行业板块"] = final_list
    return final_result


def get_rate_rank_concept():
    final_result = {}
    final_list = []
    for j in range(10):
        url = "http://37.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222" + "&pn=" + str(j+1)
        request = SendRequest(url, headers)
        s_initial = request.get_initial_data()
        s = json.loads(s_initial)
        data_num = len(s["data"]["diff"])

        for i in range(data_num):
            temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                         "涨跌额": str(s["data"]["diff"][i]["f14"]),
                         "总市值": Number_util.num_check(s["data"]["diff"][i]["f20"]),
                         "换手率": str(s["data"]["diff"][i]["f8"]) + "%", "上涨家数": str(s["data"]["diff"][i]["f104"]),
                         "下跌家数": str(str(s["data"]["diff"][i]["f105"])),
                         "最新价": str(s["data"]["diff"][i]["f2"]), "领涨股": str(s["data"]["diff"][i]["f128"]),
                         "代码": str(s["data"]["diff"][i]["f140"]), "领涨股涨幅": str(s["data"]["diff"][i]["f136"]) + "%"}
            final_list.append(temp_dict)
    final_result["概念板块"] = final_list
    return final_result


def get_rate_rank_concept_top6():
    final_result = {}
    final_list = []
    url = "http://37.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&pn=1"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    for i in range(6):
        temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                     "领涨股": str(s["data"]["diff"][i]["f128"])}
        final_list.append(temp_dict)
    final_result["概念板块"] = final_list
    return final_result


def get_money_rank_top5():
    url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&stat=1&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    data_num = len(s["data"]["diff"])
    final_result = {}
    final_list = []
    if data_num >= 5:
        for i in range(5):
            temp_dict = {s["data"]["diff"][i]["f14"]: Number_util.num_check(s["data"]["diff"][i]["f62"])}
            final_list.append(temp_dict)
    else:
        for i in range(5):
            temp_dict = {s["data"]["diff"][i]["f14"]: Number_util.num_check(s["data"]["diff"][i]["f62"])}
            final_list.append(temp_dict)
    final_result["资金流入最多"] = final_list
    return final_result


def get_fiveday_rate_rank_top5():
    url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid=f109&fs=m:90+t:2&stat=5&fields=f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124&rt=52765509"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    data_num = len(s["data"]["diff"])
    final_result = {}
    final_list = []
    if data_num >= 5:
        for i in range(5):
            temp_dict = {s["data"]["diff"][i]["f14"]: str(s["data"]["diff"][i]["f109"])+"%"}
            final_list.append(temp_dict)
    else:
        for i in range(5):
            temp_dict = {s["data"]["diff"][i]["f14"]: str(s["data"]["diff"][i]["f109"]) + "%"}
            final_list.append(temp_dict)
    final_result["5日涨幅最大"] = final_list
    return final_result


def get_top5_collections(request):
    try:
        final_result = {"code": 200,
                        "data": [get_rate_rank_top5(), get_money_rank_top5(), get_fiveday_rate_rank_top5()]}
        if get_rate_rank_top5() is not None and get_money_rank_top5() is not None and get_fiveday_rate_rank_top5() is not None:
            return JsonResponse(final_result, safe=False)
        else:
            return JsonResponse({"code": 404, "data": "资源貌似不见了"}, safe=False)
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)


def get_plate_collections(request):
    try:
        final_result = {"code": 200,
                        "data": [get_rate_rank_industry(), get_rate_rank_concept(), get_rate_rank_region()]}
        if get_rate_rank_industry() is not None and get_rate_rank_concept() is not None and get_rate_rank_region() is not None:
            return JsonResponse(final_result, safe=False)
        else:
            return JsonResponse({"code": 404, "data": "资源貌似不见了"}, safe=False)
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)


def get_rate_rank_region():
    final_result = {}
    final_list = []
    for j in range(2):
        url = "http://72.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:1&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222" + "&pn=" + str(j+1)
        request = SendRequest(url, headers)
        s_initial = request.get_initial_data()
        s = json.loads(s_initial)
        data_num = len(s["data"]["diff"])

        for i in range(data_num):
            temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                         "涨跌额": str(s["data"]["diff"][i]["f14"]),
                         "总市值": Number_util.num_check(s["data"]["diff"][i]["f20"]),
                         "换手率": str(s["data"]["diff"][i]["f8"]) + "%", "上涨家数": str(s["data"]["diff"][i]["f104"]),
                         "下跌家数": str(str(s["data"]["diff"][i]["f105"])),
                         "最新价": str(s["data"]["diff"][i]["f2"]), "领涨股": str(s["data"]["diff"][i]["f128"]),
                         "代码": str(s["data"]["diff"][i]["f140"]), "领涨股涨幅": str(s["data"]["diff"][i]["f136"])}
            final_list.append(temp_dict)
    final_result["地域板块"] = final_list
    return final_result


def get_rate_rank_region_top6():
    final_result = {}
    final_list = []
    url = "http://72.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:1&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&pn=1"
    request = SendRequest(url, headers)
    s_initial = request.get_initial_data()
    s = json.loads(s_initial)
    for i in range(6):
        temp_dict = {"名称": str(s["data"]["diff"][i]["f14"]), "涨幅": str(s["data"]["diff"][i]["f3"]) + "%",
                     "领涨股": str(s["data"]["diff"][i]["f128"])}
        final_list.append(temp_dict)
    final_result["地域板块"] = final_list
    return final_result


def get_plates_top6(request):
    try:
        return JsonResponse({"code": 200, "data": [get_rate_rank_industry_top6(), get_rate_rank_concept_top6(), get_rate_rank_region_top6()]}, safe=False)
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)


def get_hkstock_list(request):
    page_number = request.GET['PageNumber']
    url = "http://4.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:116+t:3&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152" + "&pn=" + str(page_number)
    try:
        response = SendRequest(url, headers)
        data_initial = json.loads(response.get_initial_data())
        stock_data = []
        for i in range(len(data_initial["data"]["diff"])):
            temp_dict = {"代码": str(data_initial["data"]["diff"][i]["f12"]), "股票名称": str(data_initial["data"]["diff"][i]["f14"]),
                         "最新": str(data_initial["data"]["diff"][i]["f2"]), "涨跌幅": str(data_initial["data"]["diff"][i]["f3"]) + "%",
                         "涨跌额": str(data_initial["data"]["diff"][i]["f4"]), "今开": str(data_initial["data"]["diff"][i]["f17"]),
                         "最高": str(data_initial["data"]["diff"][i]["f15"]), "最低": str(data_initial["data"]["diff"][i]["f16"]),
                         "昨收": str(data_initial["data"]["diff"][i]["f18"]), "成交量（股）": Number_util.num_check(data_initial["data"]["diff"][i]["f5"]),
                         "成交额（港元）": Number_util.num_check(data_initial["data"]["diff"][i]["f6"])
                         }
            stock_data.append(temp_dict)
        final_result = {"code": 200, "page": 107, "data": stock_data}
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)
    return JsonResponse(final_result, safe=False)


def get_mainforce_money_top6(request):
    url_industry = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f12,f13,f14,f62&fid=f62&fs=m:90+t:2&ut=b2884a393a59ad64002292a3e90d46a5"
    url_concept = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f12,f13,f14,f62&fid=f62&fs=m:90+t:3&ut=b2884a393a59ad64002292a3e90d46a5"
    url_region = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&po=1&np=1&fields=f12,f13,f14,f62&fid=f62&fs=m:90+t:1&ut=b2884a393a59ad64002292a3e90d46a5"
    try:
        response_industry, response_concept, response_region = SendRequest(url_industry, headers), SendRequest(url_concept, headers), SendRequest(url_region, headers)
        data_industry = json.loads(response_industry.get_initial_data())
        data_concept = json.loads(response_concept.get_initial_data())
        data_region = json.loads(response_region.get_initial_data())
        industry_dict, concept_dict, region_dict = {"title": "行业主力净流入"}, {"title": "概念主力净流入"}, {"title": "地域主力净流入"}

        for i in range(6):
            industry_dict[data_industry["data"]["diff"][i]["f14"]] = Number_util.num_check(data_industry["data"]["diff"][i]["f62"])
            concept_dict[data_concept["data"]["diff"][i]["f14"]] = Number_util.num_check(data_concept["data"]["diff"][i]["f62"])
            region_dict[data_region["data"]["diff"][i]["f14"]] = Number_util.num_check(data_region["data"]["diff"][i]["f62"])

        final_result = {"code": 200, "data": [industry_dict, concept_dict, region_dict]}
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse(final_result, safe=False)


def get_AHstocks_list(request):
    final_list = []
    page_number = request.GET["PageNumber"]
    try:
            url = "http://58.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:DLMK0101&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f191,f192,f193,f186,f185,f187,f189,f188" + "&pn=" + str(
                page_number)
            response = SendRequest(url, headers)
            response_data = json.loads(response.get_initial_data())

            for j in range(len(response_data["data"]["diff"])):
                final_list.append(
                    {"股票名称": response_data["data"]["diff"][j]["f14"], "港股代码": response_data["data"]["diff"][j]["f12"],
                     "A股代码": response_data["data"]["diff"][j]["f191"],
                     "最新": str(response_data["data"]["diff"][j]["f186"]) + "," + str(
                         response_data["data"]["diff"][j]["f2"]),
                     "涨幅": str(response_data["data"]["diff"][j]["f187"]) + "%," + str(
                         response_data["data"]["diff"][j]["f3"]) + "%",
                     "溢价（A/H）": str(response_data["data"]["diff"][j]["f188"]) + "%"
                     })
    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse({"code": 200, "page": 6, "data": final_list}, safe=False)


def get_ChuangYeBoard_list(request):
    final_list = []
    page_number = request.GET["PageNumber"]
    try:
        url = "http://77.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:116+t:4&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152" + "&pn=" + str(page_number)
        response = SendRequest(url, headers)
        response_data = json.loads(response.get_initial_data())

        for j in range(len(response_data["data"]["diff"])):
            final_list.append({"股票名称": response_data["data"]["diff"][j]["f14"], "代码": response_data["data"]["diff"][j]["f12"],
                               "最新": str(response_data["data"]["diff"][j]["f2"]), "涨跌额": str(response_data["data"]["diff"][j]["f4"]),
                               "涨跌幅": str(response_data["data"]["diff"][j]["f3"])+"%", "今开": str(response_data["data"]["diff"][j]["f16"]),
                               "最高": str(response_data["data"]["diff"][j]["f15"]), "最低": str(response_data["data"]["diff"][j]["f17"]),
                               "昨收": str(response_data["data"]["diff"][j]["f18"]), "成交量（股）": Number_util.num_check(response_data["data"]["diff"][j]["f5"]),
                               "成交额（港元）": Number_util.num_check(response_data["data"]["diff"][j]["f6"])
                               })

    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse({"code": 200, "page": 20, "data": final_list}, safe=False)


def get_wellknown_HKStocks(request):
    final_list = []
    page_number = request.GET["PageNumber"]
    try:
        url = "http://40.push2.eastmoney.com/api/qt/clist/get?pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:MK0106&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152" + "&pn=" + str(page_number)
        response = SendRequest(url, headers)
        response_data = json.loads(response.get_initial_data())

        for j in range(len(response_data["data"]["diff"])):
            final_list.append({"股票名称": response_data["data"]["diff"][j]["f14"], "代码": response_data["data"]["diff"][j]["f12"],
                               "最新": str(response_data["data"]["diff"][j]["f2"]), "涨跌额": str(response_data["data"]["diff"][j]["f4"]),
                               "涨跌幅": str(response_data["data"]["diff"][j]["f3"])+"%", "今开": str(response_data["data"]["diff"][j]["f16"]),
                               "最高": str(response_data["data"]["diff"][j]["f15"]), "最低": str(response_data["data"]["diff"][j]["f17"]),
                               "昨收": str(response_data["data"]["diff"][j]["f18"]), "成交量（股）": Number_util.num_check(response_data["data"]["diff"][j]["f5"]),
                               "成交额（港元）": Number_util.num_check(response_data["data"]["diff"][j]["f6"])
                               })

    except Exception:
        return JsonResponse({"code": 400, "data": "网络出问题了"}, safe=False)

    return JsonResponse({"code": 200, "page": 5, "data": final_list}, safe=False)









