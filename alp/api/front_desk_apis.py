
from flask import request, make_response, render_template, redirect
from miniagent import api, app, configure
from flask_restful import reqparse
from flask_api import status
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource
from datetime import datetime, timedelta
import uuid

@app.route('/front/join_game')
def join_game_page():
    
    account_id = request.cookies.get('alp_account_id')
    #expires = request.cookies.get('alp_account_id_expires')
    event_id = configure['C_EVENT_ID']

    if not account_id:
        #account_id = uuid.uuid4().hex[-12:]
        #resp = make_response(render_template('join_game.html',event_id=event_id))
        #resp.set_cookie('alp_account_id', account_id, max_age=timedelta(minutes=10), httponly=True, domain='localhost')
        #return resp
        return make_response(render_template('join_game.html',event_id=event_id))
    else:
        #print("no account it")
        return redirect("/front/transfer") 

@app.route('/front/transfer')
def transfer_page():

    event_id = configure['C_EVENT_ID']
    account_id = request.cookies.get('alp_account_id')

    if not account_id:
        return redirect("/front/join_game")
    
    resp = make_response(render_template('transfer.html',event_id=event_id, account_id=account_id))
    return resp