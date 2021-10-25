from datetime import datetime as dt
import pytz
def convert_stamp(stamp:str):
    """
    this function converts a timestamp in string format into a number between 0 and 9 (other values possible depending on whether or not market is acc open)
    measured in hours representing how far into the market day we are.
    the timestamps format will be: yyyy-mm-dd hh:mm:ss; For example: 2021-10-22 19:55:00
    """
    stamp_obj = dt.strptime(stamp, "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("America/New_York"))
    hh = stamp_obj.hour
    mm = stamp_obj.minute
    stamp_idx =  (hh-9) + (mm-30)/60
    return round(stamp_idx, 2)

if __name__ == '__main__':
    print(convert_stamp("2021-10-22 19:55:00"))