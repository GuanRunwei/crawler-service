import jieba
import os
from django.http import JsonResponse

jieba.load_userdict(os.path.join(os.getcwd(), r'files/股票数据.txt'))
stopwords_path = os.path.join(os.getcwd(), r'files/中文停用词表.txt')


def stopwords_list():
    with open(stopwords_path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            yield line.strip()


def cut_sentence(request):
    sentence = request.GET["Sentence"]
    seg_list = jieba.cut_for_search(sentence)
    final_result = ""
    for word in seg_list:
        if word in stopwords_list():
            continue
        final_result += word + ' '
    return JsonResponse({'code': 200, 'data': final_result}, safe=False)





