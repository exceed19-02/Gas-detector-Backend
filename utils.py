from pytz import timezone
import datetime


BANGKOK_TZ = timezone("Asia/Bangkok")


def get_bangkok_time():
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.astimezone(BANGKOK_TZ)
