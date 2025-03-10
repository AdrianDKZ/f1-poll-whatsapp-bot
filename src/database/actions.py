import sqlite3, json, datetime
import locale
from sqlmodel import Session, select
from pydantic import BaseModel

from .. import constants, utils
from . import model as db

# Set the Spanish locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class TeamPoints(BaseModel):
    name: str
    user1: str
    user2: str
    points: int
    strikes: int

### DATABASE ACTIONS

def retrieve_first(statement):
    with Session(db.engine) as session:
        return session.exec(statement).first()

def retrieve_all(statement):
    with Session(db.engine) as session:
        return session.exec(statement).all()
    
def retrieve_by_id(db_object, id):
    with Session(db.engine) as session:
        return session.get(db_object, id)
    
def commit(item):
    with Session(db.engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    
### DATABASE READ COMMANDS

def session_statement(gp_id, session_type = None, now: bool = False):
    statement = select(db.Sessions).where(db.Sessions.gp_id == gp_id)
    if session_type:
        statement = statement.where(db.Sessions.type == session_type)
    if now:
        statement = statement.where(db.Sessions.datetime > datetime.datetime.now())
    return statement

def obtain_gp():
    today = datetime.date.today()
    statement = select(db.GP).where(db.GP.date_start <= today).where(db.GP.date_finish >= today)
    return retrieve_first(statement)

def obtain_gp_times():
    gp = obtain_gp()
    if not gp:
        return constants.ERRORS["NoGP"]
    sessions = obtain_all_sessions(gp.id)
    return gp.name, sessions

def obtain_session(gp_id, session_type):
    statement = session_statement(gp_id, session_type)
    return retrieve_first(statement)

def obtain_current_session(gp_id, session_type):
    statement = session_statement(gp_id, session_type, True)
    return retrieve_first(statement)

def obtain_all_sessions(gp_id):
    statement = session_statement(gp_id)
    return retrieve_all(statement)

def obtain_session_id(session, get_session):
    gp = obtain_gp()
    if not gp:
        return constants.ERRORS["NoGP"]
    gp_session = get_session(gp.id, session)
    if not gp_session:
        return constants.ERRORS["NoSession"]
    return gp_session.id

def obtain_session_preds(session_id) -> list[db.Predictions]:
    statement = select(db.Predictions).where(db.Predictions.session_id == session_id)
    return retrieve_all(statement)

def obtain_user(telephone) -> db.Users|None:
    return retrieve_by_id(db.Users, telephone)

def obtain_polls(session):
    session_id = obtain_session_id(session, obtain_current_session) if isinstance(session, str) else session
    if utils.isError(session_id):
        return session_id  
    ## Obtain session info
    db_session = retrieve_by_id(db.Sessions, session_id)
    db_race = retrieve_by_id(db.GP, db_session.gp_id)

    preds_str = f"*!GP de {db_race.name}* \n _{db_session.type.value.capitalize()}_"
    for prediction in obtain_session_preds(session_id):
        user = obtain_user(prediction.user_id)
        pred = json.loads(prediction.prediction)
        user_pred_str = "\n".join(f"{position}- {pilot}" for position, pilot in pred.items())
        preds_str += f"\n\n{user.name}:\n{user_pred_str}"
    return preds_str

def obtain_user_points():
    users: db.Users = retrieve_all(select(db.Users))
    users_lst = sorted(users, key=lambda x: (-x.points, -x.strikes))
    return "*Porra Individual*\n" + "\n".join(f"{user.name} - {user.points} puntos ({user.strikes})" for user in users_lst)


def obtain_team_points():
    teams_info: list[TeamPoints] = []
    for team in retrieve_all(select(db.Teams)):
        user1, user2 = obtain_user(team.user1), obtain_user(team.user2)
        teams_info.append(TeamPoints(name=team.name, user1=user1.name, user2=user2.name, points=user1.points+user2.points, strikes=user1.strikes+user2.strikes))
    teams_info = sorted(teams_info, key=lambda x: (-x.points, -x.strikes))
    return "*Porra por Equipos*\n" + "\n".join(f"{team.name} ({team.user1} y {team.user2}) - {team.points} puntos ({team.strikes})" for team in teams_info)

### DATABASE WRITE ACTIONS 

def store_results(prediction, session_id):
    gp_session: db.Sessions = retrieve_by_id(db.Sessions, session_id)
    gp_session.result = json.dumps(prediction)
    commit(gp_session)

def store_user(telephone, user_name):
    user = obtain_user(telephone)
    if not user:
        name = f"@{telephone}" if user_name == "" else user_name.split(" ")[0]
        commit(db.Users(telephone=telephone, name=name))

def store_poll(prediction, session, user):
    session_id = obtain_session_id(session, obtain_current_session)
    if utils.isError(session_id):
        return session_id
    
    user_id = obtain_user(user).telephone

    statement = select(db.Predictions).where(db.Predictions.session_id == session_id).where(db.Predictions.user_id == user_id)
    db_item = retrieve_first(statement)

    db_prediction = db.Predictions(session_id=session_id, user_id=user_id, prediction="") if not db_item else db_item
    db_prediction.prediction = json.dumps(prediction) 
    commit(db_prediction)

    session_time = utils.dt_to_msg(retrieve_by_id(db.Sessions, session_id).datetime)

    response = "!Predicción actualizada" if db_item else "!Prediccion guardada"
    return f"{response} \nLímite porra: {session_time}"


def prediction_points(results, session):
    print(results)
    session_id = obtain_session_id(session, obtain_session)
    if utils.isError(session_id):
        return session_id   
    ## Store session results
    store_results(results, session_id)
    ## Obtain all predictions made for session
    resultados = "*Puntos obtenidos*"
    for prediction in obtain_session_preds(session_id):
        ## Obtain user points and strikes
        points, strike = get_points(prediction.prediction, results, session)
        ## Get previous points if result had already been indicated
        prev_points = 0 if prediction.points == None else prediction.points
        prev_strike = 1 if prev_points >= 5 else 0
        ## Update prediction points
        prediction.points = points
        commit(prediction)
        ## Obtain historical points and strikes
        user_info = obtain_user(prediction.user_id)
        ## Update total points and strikes. Obtained points + Total points - Previous session points (normally this will be 0)
        user_info.points = points + user_info.points - prev_points
        user_info.strikes = strike + user_info.strikes - prev_strike
        commit(user_info)
        resultados += f"\n{user_info.name}: {points} pts."
    return resultados      

def get_points(prediction, results, session):
    ## Strike is a boolean int, so it can be added outside the function
    points, strike = 0, 1
    prediction = json.loads(prediction)
    for position, pilot in results.items():
        ## Add point if hit
        if prediction[position] == pilot:
            points += 1
        ## Strike to false if fail at a numeric position or not a race
        elif position != "ALO":
            strike = 0
    ## Two extra points if strike
    strike = 0 if session != "carrera" else strike
    points += 2 if strike else 0
    return points, strike
