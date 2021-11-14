from django.urls import path
import controller.get_data
import controller.get_panmian
import controller.get_winnerlist
import controller.get_worldstocks
import controller.get_kechuang
import controller.get_cutwords
import controller.get_file
import controller.get_model_result

urlpatterns = [
    path('get_top5_collections', controller.get_data.get_top5_collections),
    path('get_plate_collections', controller.get_data.get_plate_collections),
    path('get_hkstock_list', controller.get_data.get_hkstock_list),
    path('get_mainforce_money_top6', controller.get_data.get_mainforce_money_top6),
    path('get_plates_top6', controller.get_data.get_plates_top6),
    path('get_AHstocks_list', controller.get_data.get_AHstocks_list),
    path('get_ChuangYeBoard_list', controller.get_data.get_ChuangYeBoard_list),
    path('get_wellknown_HKStocks', controller.get_data.get_wellknown_HKStocks),
    path('get_yidong', controller.get_panmian.get_yidong),
    path('get_single_plate', controller.get_data.get_single_plate),
    path('get_winnerlist', controller.get_winnerlist.get_winnerlist),
    path('get_worldstock_index', controller.get_worldstocks.get_worldstock_index),
    path('get_kechuang', controller.get_kechuang.get_kechuang),
    path('cut_sentence', controller.get_cutwords.cut_sentence),
    path('get_file', controller.get_file.get_picture),
    path('get_model_result', controller.get_model_result.get_CNN_result),
    path('get_model_result2', controller.get_model_result.get_CNN_result)
]
