import re

def process_poll(poll, session, user):
    for pred in poll:
        pred_info = pred.split("-")
        if "alo" in pred_info[0]:
            position = int(re.sub("[a-zA-Z]+", " ", pred_info[1]))
            print(f"alo: {position}")
        else:
            position = int(pred_info[0])
            print(position)
