from ..model.account import Account
from sqlalchemy import or_
from sqlalchemy.sql import insert
from miniagent import db
from miniagent.common import now

def insert_account(data: dict):

    insert_dict = data.copy()
    insert_dict.update(dict(
        created_date = now()
    ))
    stmt = insert(Account).values(**insert_dict)
    db.session.execute(stmt)

def select_accounts(event_id: str):

    reqs = Account.query\
        .filter(or_(Account.event_id == event_id, event_id=='all')).all()
    
    return reqs