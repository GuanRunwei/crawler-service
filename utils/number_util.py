import math


class Number_util(object):

    @staticmethod
    def num_check(num):
        try:
            if num >= 0:
                if len(str(int(num))) > 8:
                    return str(round(num / (pow(10, 8)), 2)) + "亿"
                if 4 < len(str(int(num))) <= 8:
                    return str(round(num / (pow(10, 4)), 2)) + "万"
                return str(num)
            else:
                if len(str(int(math.fabs(num)))) > 8:
                    return "-" + str(round(math.fabs(num) / (pow(10, 8)), 2)) + "亿"
                if 4 < len(str(int(math.fabs(num)))) <= 8:
                    return "-" + str(round(math.fabs(num) / (pow(10, 4)), 2)) + "万"
                return str(num)

        except Exception:
            return "-"

    @staticmethod
    def convert_stringnumber(str_num):
        try:
            if float(str_num) >= 0:
                if len(str_num) > 8:
                    return str(round(float(str_num) / (pow(10, 8)), 2)) + "亿"
                if 4 < len(str_num) <= 8:
                    return str(round(float(str_num) / (pow(10, 4)), 2)) + "万"
                return str_num
            else:
                if len(str(math.fabs(float(str_num)))) > 8:
                    return "-" + str(round(math.fabs(float(str_num)) / (pow(10, 8)), 2)) + "亿"
                if 4 < len(str(math.fabs(int(str_num)))) <= 8:
                    return "-" + str(round(math.fabs(float(str_num)) / (pow(10, 4)), 2)) + "万"
                return str_num

        except Exception:
            return "-"

