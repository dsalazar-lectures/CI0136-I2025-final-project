import pytz
from datetime import datetime

def get_current_datetime():
    cr_timezone = pytz.timezone("America/Costa_Rica")
    return datetime.now(cr_timezone).replace(second=0, microsecond=0)