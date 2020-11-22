from src.com.stock.common.import_lib import *


def make_year_list (start_year, end_year):
    result = []
    start_year = int(start_year)
    end_year = int(end_year)


    delta = end_year - start_year
    if delta <0:
        print("년도 입력 오류")
    elif delta >0:
        for i in range(delta):
            result.append(str(int(start_year) + i))
    else:
        result.append(start_year)
    return  result

def get_kr_working_day_by_diff(input_working_date, diff):
    year = input_working_date.strftime("%Y%m%d")[:4]
    year_list = make_year_list(year , year)
    kr_holiday = get_holiday(year_list, "ALL")
    target_date = input_working_date
    if diff == 0 :
        return input_working_date
    elif diff < 0:
        while diff != 0:
            target_date = target_date - timedelta(days= abs(diff))
            if is_red_day(target_date):
                continue
            elif target_date.strftime("%Y%m%d") in kr_holiday:
                continue
            else:
                diff = diff+1
        return target_date
    else:
        while diff != 0:
            target_date = target_date + timedelta(days= abs(diff))
            if is_red_day(target_date):
                continue
            elif target_date.strftime("%Y%m%d") in kr_holiday:
                continue
            else:
                diff = diff-1
        return target_date


def make_date_list (start_date, end_date):
    #YYYYMMDD
    d1 = date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
    d2 = date (int(end_date[:4]), int(end_date[4:6]), int(end_date[6:]))
    delta = d2 - d1

    date_list = []
    for i in range(delta.days +1 ):
        date_list.append((d1 + timedelta(days=i)))
    return date_list
def get_kr_working_day(start_date, end_date):
    date_list = make_date_list(start_date, end_date)
    year_list = make_year_list(start_date[:4], end_date[:4])
    kr_holiday = get_holiday(year_list, "ALL")
    result = []
    for i in date_list:
        if is_red_day(i):
            continue
        elif i in kr_holiday:
            continue
        else:
            result.append(i)

    return result

if __name__ == "__main__":
    test_date = datetime(2020,8,18)
    test_date2 = get_kr_working_day_by_diff(test_date, -1)

    print(test_date)
    print(test_date2)