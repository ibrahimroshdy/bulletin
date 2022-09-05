import datetime

from uptime import uptime


def machine_uptime_func():
    uptime_timedelta = datetime.timedelta(seconds=uptime())
    uptime_dict = {"days": uptime_timedelta.days}
    uptime_dict["hours"], rem = divmod(uptime_timedelta.seconds, 3600)
    uptime_dict["minutes"], uptime_dict["seconds"] = divmod(rem, 60)
    return uptime_dict
