import json
import math
import datetime

from easymoney_crawler.settings import BASE_DIR
from util.SendRequest import SendRequest
from util.number_util import Number_util
import shutil
import os
from django.http import JsonResponse

file_path = "./img/"


def get_picture(request):
    if request.method == 'POST':
        print("文件个数：", len(request.FILES))
        print(request.FILES["file"])
        if request.FILES:
            picture_obj = request.FILES["file"]
            datetime_string = datetime.datetime.now().strftime('%Y%m%d%H%M')
            path = file_path + str(picture_obj.name).split(".")[0] + "time" + datetime_string + ".png"
            with open(path, 'wb') as f:
                for content in picture_obj.chunks():
                    f.write(content)

            return JsonResponse({"code": 200, "data": file_path + str(picture_obj.name).split(".")[0] + "time" + datetime_string + ".png"}, safe=False)
    return JsonResponse({"code": 400, "data": "bad"}, safe=False)