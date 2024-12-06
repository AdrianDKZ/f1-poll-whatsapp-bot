import datetime as dt
import constants

def str_to_dt(datetime):
    return dt.datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')

def dt_to_msg(datetime):
    return str_to_dt(datetime).strftime('%A %d, %H:%M').capitalize()

def isError(msg):
    return True if isinstance(msg, str) else False

def build_msg():
    from neonize.utils import build_jid
    return build_jid(constants.CHAT_ID, "g.us")
    