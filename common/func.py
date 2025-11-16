# 公用函数

from datetime import datetime, timezone, timedelta

# 时区
utc = timezone(timedelta(hours=8))

# test
def test(txt):
    print("公用函数test()：" + txt)
    return txt

# 时间日期
def get_date(format="%Y-%m-%d %H:%M:%S %p %A %B"):
    return datetime.now(utc).strftime(format)

# 获取毫秒时间
def get_time_ms():
    return datetime.now(utc).microsecond // 1000

# 获取秒时间
def get_time_s():
    return datetime.now(utc).microsecond // 1000 // 1000
