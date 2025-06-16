from datetime import datetime

def get_current_datetime():
    # Returns the current date and time.   
    return datetime.now().replace(second=0, microsecond=0)