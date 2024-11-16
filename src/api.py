import requests, datetime as dt

sessions = {
    "FirstPractice": "libres",
    "SecondPractice": "libres",
    "ThirdPractice": "libres",
    "Qualifying": "qualy",
    "Sprint": "sprint"
}

url = "https://ergast.com/api/f1/2024.json"
response = requests.get(url)
season = response.json()["MRData"]["RaceTable"]["Races"]

## Combine date and time and transform from UTC to system TZ
def format_dt(date: str, time: str):
    full_date = dt.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%SZ')
    return full_date.replace(tzinfo=dt.timezone.utc).astimezone(tz=None)

def format_str(datetime: dt.datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')


for race in season:
    race_dt = format_dt(race["date"], race["time"])
    ## Obtain race week start (tuesday) and end (monday)
    days_to_start = (race_dt.weekday() - 1) % 7
    gp_start = race_dt - dt.timedelta(days_to_start)
    gp_end = gp_start + dt.timedelta(days=6)
    ## Obtain race sessions and times
    gp_sessions = []
    for race_session, session_times in race.items():
        if race_session in sessions.keys():
            ## if Practise2 and Sprint, it is Sprint Qualy
            if race_session == "SecondPractice" and "Sprint" in race.keys():
                session_name = "squaly"
            else:
                session_name = sessions[race_session]
            gp_sessions.append((session_name, format_str(format_dt(session_times['date'], session_times['time']))))
    gp_sessions.append(("carrera", format_str(race_dt)))
    print()
    


