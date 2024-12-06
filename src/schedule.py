import datetime as dt, time
from scheduler import Scheduler
from scheduler.trigger import Tuesday, Friday

from neonize.client import NewClient

import commit_database, utils

def send_message(message):
    client.send_message(utils.build_msg(), message)

def race_week():
    times_info = commit_database.obtain_times()
    if utils.isError(times_info):
        return
    from commands import format_times    
    send_message(format_times(times_info))

def session_scheduler():
    times_info = commit_database.obtain_times()
    if utils.isError(times_info):
        return
    for session in times_info[1]:
        session_dt = utils.str_to_dt(session[2])
        if session_dt > dt.datetime.now():
            schedule.once(session_dt, print_poll, kwargs={"session_id": session[0]})
    
def print_poll(session_id):
    send_message(commit_database.obtain_polls(session_id))

def schedule_runner(client_: NewClient):
    global schedule, client
    schedule, client = Scheduler(), client_
    schedule.weekly(Tuesday(dt.time(9, 30)), race_week)
    schedule.weekly(Friday(), session_scheduler)
    if dt.date.today().weekday() >= 4:
        session_scheduler()
    print(schedule, flush=True)
    while True:
        schedule.exec_jobs()
        time.sleep(1)