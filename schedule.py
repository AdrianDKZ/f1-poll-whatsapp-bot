import threading, time
from datetime import datetime
from scheduler import Scheduler
from scheduler.trigger import Friday

from neonize.client import NewClient
from neonize.utils import build_jid

import commit_database
import constants

def session_scheduler():
    times_info = commit_database.obtain_times()
    if isinstance(times_info, str):
        return
    for session in times_info[1]:
        session_dt = datetime.strptime(session[2], '%Y-%m-%d %H:%M:%S')
        schedule.once(session_dt, print_poll, kwargs={"session_id": session[0]})
    
def print_poll(session_id):
    client.send_message(build_jid(constants.CHAT_ID, "g.us"), (commit_database.obtain_polls(session_id)))

def schedule_runner(client_: NewClient):
    global schedule, client
    schedule, client = Scheduler(), client_
    schedule.weekly(Friday(), session_scheduler)
    while True:
        schedule.exec_jobs()
        time.sleep(1)