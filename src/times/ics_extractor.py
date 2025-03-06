from ics import Calendar
import datetime as dt
import pytz, re

from ..database import database as db
from sqlmodel import select, Session


categories = {
            "Entrenamientos Libres 1": db.Session_Type.LIBRES.value, 
            "Entrenamientos Libres 2": db.Session_Type.LIBRES.value,
            "Entrenamientos Libres 3": db.Session_Type.LIBRES.value, 
            "Clasificación": db.Session_Type.QUALY.value, 
            "Gran Premio": db.Session_Type.CARRERA.value,
            "Sprint Qualifying": db.Session_Type.SQUALY.value, 
            "Sprint": db.Session_Type.SPRINT.value}


ics_file = "src/times/f1-calendar_p1_p2_p3_qualifying_sprint_gp.ics"
calendar = Calendar(open(ics_file).read())

with Session(db.engine) as session:
    for event in sorted(calendar.events):
        ## Obtain event data
        event_type = categories[(event.categories & categories.keys()).pop()]
        event_dt = event.begin.astimezone(pytz.timezone('Europe/Madrid'))

        ## Obtain database GP
        gp_name = re.search(r'Gran Premio de (.*?)\)', event.name).group(1)
        db_gp = session.exec(select(db.GP).where(db.GP.name == gp_name)).first()
        if not db_gp:
            ## Obtain GP data
            days_to_start = (event_dt.weekday() - 1) % 7
            gp_start = (event_dt - dt.timedelta(days_to_start))
            gp_end = gp_start + dt.timedelta(days=6)
            ## Create DB object
            db_gp = db.GP(name=gp_name, date_start=gp_start.date(), date_finish=gp_end.date())
            session.add(db_gp)
            session.commit()
            session.refresh(db_gp)

        ## Create database Sessions
        db_event = db.Sessions(gp_id=db_gp.id, datetime=event_dt, type=event_type)
        session.add(db_event)
        session.commit()
    session.commit()
