
from flask import request, make_response, render_template, redirect
from miniagent import api, app, configure
from flask_restful import reqparse
from flask_api import status
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource
from datetime import datetime, timedelta
import uuid
import json
import logging

import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams

@app.route('/front/join_game')
def join_game_page():
    
    #account = request.cookies.get('alp_account_id')
    account = request.cookies.get('account_id')
    #expires = request.cookies.get('alp_account_id_expires')
    event_id = configure['C_EVENT_ID']

    logging.warning(account)
    if not account:
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

    front_version = configure['C_FRONT_VERSION']
    event_id = configure['C_EVENT_ID']
    #account_str = request.cookies.get('alp_account_id')
    #logging.error(account_str)
    #if not account_str:
    #    return redirect("/front/join_game")

    account_id = request.cookies.get('account_id')
    user_name = request.cookies.get('user_name')
    
    """
    account_dict = json.loads(account_str)
    resp = make_response(render_template('transfer.html',
                                         event_id=event_id, 
                                         account_id=account_dict['account_id'],
                                         user_name=account_dict['user_name'],
                                         version=front_version
                                         ))
    """
    resp = make_response(render_template('transfer.html',
                                         event_id=event_id, 
                                         account_id=account_id,
                                         user_name=account_id,
                                         version=front_version
                                         ))

    return resp

@app.route("/front/stat")
def stat():

    event_id = configure['C_EVENT_ID']

    data = dict(
        initial_param = {"event_id":event_id},
        executer = 'alp.executer.front_desk.Stat',
    )

    rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

    if rtn <= 0:

        return rtn_message, status.HTTP_400_BAD_REQUEST

    #font_path = "/home/hennry/.local/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/NanumGothic.ttf"
    #font_name = fm.FontProperties(fname=font_path).get_name()
    #plt.rcParams["font.family"] = font_name
    plt.rcParams["font.family"] = "NanumGothic"

    data_set = rtn_message['results']
    sorted_data = sorted(data_set, key=lambda x: x['tot_tran_amount'], reverse=False)

    """
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    """
    user_names = [entry['user_name'] for entry in sorted_data]
    tran_amounts = [entry['tot_tran_amount'] for entry in sorted_data]

    # Create horizontal bar chart
    plt.barh(user_names, tran_amounts, color='skyblue')
    plt.xlabel('총거래금액')
    plt.ylabel('사용자명')
    plt.title('Total Transaction Amount by User')

    buf = BytesIO()
    #fig.savefig(buf, format="png")
    fig = plt.gcf()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    #data = base64.b64encode(buf.getbuffer()).decode()
    data = base64.b64encode(buf.getvalue()).decode()
    return f"<img src='data:image/png;base64,{data}'/>"