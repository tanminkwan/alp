from flask import request, make_response, after_this_request
from flask_restful import reqparse
from miniagent.event_receiver import Resource
from flask_api import status
from miniagent import api, configure
from miniagent.executer import ExecuterCaller
from datetime import timedelta
import uuid
import json
import logging

class Accounts(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str)
    #parser.add_argument('account_id', type=str)
    
    def get(self, event_id):

        param = dict(
                initial_param = {"event_id":event_id} ,
                executer = 'alp.executer.account.AccountList',
            )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(param)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    def post(self, event_id):

        args = Accounts.parser.parse_args()
        account_id = uuid.uuid4().hex[-12:]
        
        @after_this_request
        def set_cookie(response):
            #response.set_cookie('wts_game_account_id', uuid.uuid4().hex, max_age=300, httponly=True)

            cookie_data = dict(
                account_id = account_id,
                user_name = args['user_name']
            )
            valid_period = configure['C_VALID_PERIOD'] if configure.get('C_VALID_PERIOD') else 20
            response.set_cookie('alp_account_id', json.dumps(cookie_data), max_age=timedelta(minutes=valid_period), samesite=None, httponly=True)
            return response
        
        initial_param = dict(
            user_name = args['user_name'],
            account_id = account_id,
            event_id  = event_id
        )

        param = dict(
                initial_param = initial_param ,
                executer = 'alp.executer.account.Account',
            )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(param)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    post.permitted_roles = ["account"]
    get.permitted_roles = ["account"]

api.add_resource(Accounts, '/accounts/<string:event_id>', endpoint='accounts')