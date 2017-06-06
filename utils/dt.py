import datetime

def get_today(dt_format='%Y%m%d'):
    return datetime.datetime.now().strftime(dt_format)
