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
def get_kr_str_working_day_list_by_diff(input_working_date, diff):
    if type(input_working_date) is str :
        input_working_date = dt_dt(int(input_working_date[:4]), int(input_working_date[4:6]), int(input_working_date[6:8]))
    year = input_working_date.strftime("%Y%m%d")[:4]
    year_list = make_year_list(year , year)
    kr_holiday = get_holiday(year_list, "ALL")
    target_date = input_working_date
    work_day_list = []
    if diff == 0 :
        return input_working_date
    elif diff < 0:
        while diff != 0:
            target_date = target_date - timedelta(days= abs(1))
            if target_date.strftime("%Y%m%d") == "20201231":
                continue
            elif is_red_day(target_date):
                continue
            elif target_date.strftime("%Y%m%d") in kr_holiday:
                continue
            else:
                work_day_list.append(target_date.strftime("%Y%m%d"))
                diff = diff+1
        return work_day_list
    else:
        while diff != 0:
            target_date = target_date + timedelta(days= abs(1))
            if target_date.strftime("%Y%m%d") == "20201231":
                continue
            elif is_red_day(target_date):
                continue
            elif target_date.strftime("%Y%m%d") in kr_holiday:
                continue
            else:
                work_day_list.append(target_date.strftime("%Y%m%d"))
                diff = diff-1
        return work_day_list


def get_kr_working_day_by_diff(input_working_date, diff):
    if type(input_working_date) is str:
        input_working_date = dt_dt(int(input_working_date[:4]), int(input_working_date[4:6]), int(input_working_date[6:8]))
    year = input_working_date.strftime("%Y%m%d")[:4]
    year_list = make_year_list(year , year)
    kr_holiday = get_holiday(year_list, "ALL")
    target_date = input_working_date
    if diff == 0 :
        return input_working_date
    elif diff < 0:
        while diff != 0:
            target_date = target_date - timedelta(days= abs(diff))
            if target_date.strftime("%Y%m%d") == "20201231":
                continue
            elif is_red_day(target_date):
                continue
            elif target_date.strftime("%Y%m%d") in kr_holiday:
                continue
            else:
                diff = diff+1
        return target_date
    else:
        while diff != 0:
            target_date = target_date + timedelta(days= abs(diff))
            if target_date.strftime("%Y%m%d") == "20201231":
                continue
            elif is_red_day(target_date):
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
        if i.strftime("%Y%m%d") == "20201231":
            continue
        elif is_red_day(i):
            continue
        elif i in kr_holiday:
            continue
        else:
            result.append(i)

    return result
def string_to_datetime(day, hour_min_sec):
    #day yyyymmdd
    if len(hour_min_sec) == 4:
        hour_min_sec+="00"
    result = datetime.strptime(day+hour_min_sec, "%Y%m%d%H%M%S")
    return result

if __name__ == "__main__":
    day = "20201230"

    real_TR_SCHART = make_collection("stock_data", "real_TR_SCHART")
    tr_schart_df = []
    for i in real_TR_SCHART.find({"단축코드": "000020", "일자": day}):
        tr_schart_df.append(i)
    tr_schart_df = pd.DataFrame(tr_schart_df)

    tr_schart_df_x = tr_schart_df["시간"]
    tr_schart_df_x = tr_schart_df_x.apply(lambda x: string_to_datetime(day, x))
    print(tr_schart_df_x)
