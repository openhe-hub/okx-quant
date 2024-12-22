from datetime import datetime

def str_to_timestamp_ms(date_str, format_str="%Y-%m-%d"):
    dt = datetime.strptime(date_str, format_str)
    timestamp_ms = int(dt.timestamp() * 1000)
    return timestamp_ms

def timestamp_ms_to_str(timestamp_ms, format_str="%Y-%m-%d"):
    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return dt.strftime(format_str)