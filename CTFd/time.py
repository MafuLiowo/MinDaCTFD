import datetime

def utcnow():
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)