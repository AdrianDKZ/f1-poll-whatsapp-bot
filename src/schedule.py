import threading, time
import datetime as dt
from scheduler import Scheduler
from scheduler.trigger import Tuesday, Friday

from neonize.client import NewClient
from neonize.utils import build_jid

import commit_database
from constants import CHAT_ID
from commands import format_times

def send_message(message):
    client.send_message(build_jid(CHAT_ID, "g.us"), message)

def race_week():
    times_info = commit_database.obtain_times()
    if isinstance(times_info, str):
        return
    send_message(format_times(times_info))

def session_scheduler():
    times_info = commit_database.obtain_times()
    if isinstance(times_info, str):
        return
    for session in times_info[1]:
        session_dt = dt.datetime.strptime(session[2], '%Y-%m-%d %H:%M:%S')
        schedule.once(session_dt, print_poll, kwargs={"session_id": session[0]})
    
def print_poll(session_id):
    send_message(commit_database.obtain_polls(session_id))

def schedule_runner(client_: NewClient):
    global schedule, client
    schedule, client = Scheduler(), client_
    schedule.weekly(Tuesday(dt.time(9, 30)), race_week)
    schedule.weekly(Friday(), session_scheduler)
    while True:
        schedule.exec_jobs()
        time.sleep(1)