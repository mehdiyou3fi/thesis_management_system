from datetime import datetime,timedelta
'''بررسی برای اینکه ایا 3 ماه از تاریخ ثبت پایان نامه گذشته یا نه'''

def check_three_month_passed(request_date_str):
    request_date = datetime.strptime(request_date_str,"%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    return now >= request_date +timedelta(days=90)
