import datetime as dt
from . import constants

def dt_to_msg(datetime):
    return datetime.strftime('%A %d, %H:%M').capitalize()

def isError(msg):
    return True if isinstance(msg, str) else False

def build_msg():
    from neonize.utils import build_jid
    return build_jid(constants.CHAT_ID, "g.us")
    