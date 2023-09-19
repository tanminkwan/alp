
from flask import request, make_response, render_template, redirect
from miniagent import api, app, configure
from flask_restful import reqparse
from flask_api import status
from miniagent.executer import ExecuterCaller
from miniagent.event_receiver import Resource
from datetime import datetime, timedelta
import uuid

class Transfers(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('sender', type=str)
    parser.add_argument('receiver', type=str)
    parser.add_argument('transfer_amount', type=int)

    def post(self, event_id):

        args = Transfers.parser.parse_args()

        initial_param = dict(
            sender = args['sender'],
            receiver = args['receiver'],
            transfer_amount = args['transfer_amount'],
            event_id  = event_id
        )

        param = dict(
                initial_param = initial_param ,
                executer = 'alp.executer.transfer.Transfer',
            )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(param)

        if rtn > 0:
            status_code = status.HTTP_200_OK
        elif rtn == 0:
            return rtn_message, status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return rtn_message, status_code

    post.permitted_roles = ["transfer"]

api.add_resource(Transfers, '/transfers/<string:event_id>', endpoint='transfers')